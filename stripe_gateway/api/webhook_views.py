import pytz
import stripe
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json

from accounts.models import CoursePackage
from payments.models import Customer
from stripe_gateway.models import Webhook, WebhookError


def construct_data(card):
    brand = card['brand']
    exp = f'{card["exp_month"]}/{card["exp_year"]}'
    funding = card["funding"]
    last_4 = card["last4"]

    data = f'{brand} {funding} card xxxx-{last_4}, EXP: {exp}'

    return data


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny, ])
def webhook_capture(request):
    webhook_secret = None
    request_data = request.data

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.META['HTTP_STRIPE_SIGNATURE']
        print(signature)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            event = stripe.Webhook.construct_event(
                payload=json.dumps(request_data), sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            print(e)
            return Response(data=str(e))
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    try:
        status = False if 'fail' in event_type else True
        Webhook.objects.create(
            event_id=request_data['id'],
            object_id=data_object['id'],
            customer_id=data_object['customer'],
            event_type=event_type,
            is_succeed=status,
            body=json.dumps(request_data, sort_keys=True, indent=2)
        )
    except Exception as e:
        try:
            WebhookError.objects.create(error_data=str(e))
        except Exception as e1:
            print(e1)
            pass
        print(e)
    print(event_type)
    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        subscription_price_id = data_object['lines']['data'][0]['price']['id']
        subscription_id = data_object['lines']['data'][0]['subscription']
        customer = data_object['customer']
        clear_till = data_object['lines']['data'][0]['period']['end']
        print(subscription_price_id)
        print(customer)
        try:
            package = CoursePackage.objects.get(stripe_price_id__icontains=subscription_price_id)
        except (CoursePackage.DoesNotExist, CoursePackage.MultipleObjectsReturned) as e:
            print(e)
            package = None
        print(package)
        try:
            customer = Customer.objects.get(stripe_customer_id__icontains=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None
        print(customer)
        if customer is not None and package is not None:
            customer.customer_subscription_id = subscription_id
            customer.was_created_successfully = True
            customer.last_payment_has_error = False
            customer.last_payment_error_comment = None
            customer.clear_till = timezone.datetime.fromtimestamp(clear_till, tz=pytz.UTC)
            customer.user.activate_the_user()
            customer.user.package_id = package.id
            customer.user.save()
            customer.cancel_scheduled = False
            customer.save()
            customer.user.email_user_subscription_success()

    if event_type == 'customer.subscription.updated':
        subscription_price_id = data_object['items']['data'][0]['price']['id']
        subscription_id = data_object['id']
        customer = data_object['customer']
        cancel_at_period_end = data_object['cancel_at_period_end']
        clear_till = data_object['current_period_end']

        try:
            package = CoursePackage.objects.get(stripe_price_id=subscription_price_id)
        except (CoursePackage.DoesNotExist, CoursePackage.MultipleObjectsReturned) as e:
            package = None
        try:
            customer = Customer.objects.get(stripe_customer_id=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None
        if customer is not None and package is not None:
            customer.customer_subscription_id = subscription_id
            customer.was_created_successfully = True
            customer.last_payment_has_error = False
            customer.last_payment_error_comment = None
            customer.user.activate_the_user()
            customer.user.package_id = package.id
            customer.user.save()
            customer.cancel_scheduled = cancel_at_period_end
            customer.save()
            print(subscription_price_id)
            print(customer)

        if cancel_at_period_end:
            customer.user.email_user_subscription_scheduled(timezone.datetime.fromtimestamp(clear_till, tz=pytz.UTC))

    if event_type == 'payment_intent.succeeded':
        customer = data_object['customer']
        card = data_object['charges']['data'][0]['payment_method_details']['card']
        trx_id = data_object['charges']['data'][0]['balance_transaction']
        payment_method = data_object['payment_method']
        timestamp = timezone.datetime.fromtimestamp(data_object['created'], tz=pytz.UTC)

        try:
            customer = Customer.objects.prefetch_related('payment_method_token').get(stripe_customer_id=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None

        if customer is not None:
            customer.payment_method_token.filter(stripe_payment_method_id=payment_method).update(
                is_verified=True)
            customer.user.email_user_payment_succeeded(card_data=construct_data(card), timestamp=timestamp,
                                                       trx_id=trx_id)

    if event_type == 'payment_intent.payment_failed':
        customer = data_object['customer']
        card = data_object['charges']['data'][0]['payment_method_details']['card']
        timestamp = timezone.datetime.fromtimestamp(data_object['created'], tz=pytz.UTC)
        error_msg = data_object['last_payment_error']['message']

        fingerprint = card['fingerprint']

        try:
            customer = Customer.objects.prefetch_related('payment_method_token').get(stripe_customer_id=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None

        if customer is not None:
            customer.payment_method_token.filter(payment_method_token__icontains=fingerprint).update(
                is_verified=False)
            customer.user.email_user_payment_failed(construct_data(card), timestamp, error_msg)

    if event_type == 'charge.failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        customer = data_object['customer']
        msg = data_object['failure_message']
        try:
            customer = Customer.objects.get(stripe_customer_id=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None
        if customer is not None:
            card = construct_data(data_object['payment_method_details']['card'])
            timestamp = timezone.datetime.fromtimestamp(data_object['created'], tz=pytz.UTC)
            customer.user.email_user_card_declined(card, timestamp, msg)
            customer.was_created_successfully = True
            customer.last_payment_has_error = True
            customer.last_payment_error_comment = msg
            customer.user.inactivate_the_user()
            customer.user.package = None
            customer.user.save()
            customer.save()
            print(customer)

    if event_type == 'customer.subscription.deleted':
        customer = data_object['customer']
        subscription_id = data_object['id']
        created = data_object['created']
        try:
            customer = Customer.objects.get(stripe_customer_id=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None
        if customer is not None:
            customer.user.email_user_subscription_deleted(timestamp=timezone.datetime.fromtimestamp(created, tz=pytz.UTC))
            customer.customer_subscription_id = None
            customer.was_created_successfully = True
            customer.last_payment_has_error = False
            customer.last_payment_error_comment = None
            customer.clear_till = None
            customer.cancel_scheduled = False
            customer.user.package_id = None
            customer.user.save()
            customer.cancel_scheduled = False
            customer.save()
            print(subscription_id)
            print(customer)

    return Response()
