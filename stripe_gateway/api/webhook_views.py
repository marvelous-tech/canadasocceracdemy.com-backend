import pytz

import stripe
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from django.utils import timezone

from accounts.models import CoursePackage
from payments.models import Customer, PaymentMethodToken


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

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        subscription_price_id = data_object['lines']['data'][0]['price']['id']
        subscription_id = data_object['lines']['data'][0]['subscription']
        customer = data_object['customer']
        clear_till = data_object['lines']['data'][0]['period']['end']
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
            customer.clear_till = timezone.datetime.fromtimestamp(clear_till, tz=pytz.UTC)
            customer.user.activate_the_user()
            customer.user.package_id = package.id
            customer.user.save()
            customer.save()
            print(subscription_price_id)
            print(customer)

    if event_type == 'customer.subscription.updated':
        subscription_price_id = data_object['items']['data'][0]['price']['id']
        subscription_id = data_object['items']['data'][0]['subscription']
        customer = data_object['customer']
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
            customer.save()
            print(subscription_price_id)
            print(customer)

    if event_type == 'payment_intent.succeeded':
        card = data_object['charges']['data'][0]['payment_method_details']['card']

        fingerprint = card['fingerprint']

        PaymentMethodToken.objects.filter(payment_method_token__exact=fingerprint).update(is_verified=True)

    if event_type == 'payment_intent.payment_failed':
        card = data_object['charges']['data'][0]['payment_method_details']['card']

        fingerprint = card['fingerprint']

        PaymentMethodToken.objects.filter(payment_method_token__exact=fingerprint).update(is_verified=False)

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
        try:
            customer = Customer.objects.get(stripe_customer_id=customer)
        except (Customer.MultipleObjectsReturned, Customer.DoesNotExist) as e:
            customer = None
        if customer is not None:
            customer.customer_subscription_id = None
            customer.was_created_successfully = True
            customer.last_payment_has_error = False
            customer.last_payment_error_comment = None
            customer.clear_till = None
            customer.user.inactivate_the_user()
            customer.user.package_id = None
            customer.user.save()
            customer.save()
            print(subscription_id)
            print(customer)

    return Response()
