# Create your views here.
from braintree.exceptions import NotFoundError
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import CoursePackage
from core.views import get_default_contexts
from payments.gateway import *
from payments.models import Subscription, Transaction, Customer, PaymentMethodToken


def create_method(result):
    type_ = result.payment_method.__class__.__name__
    data = getattr(result.payment_method, 'email', None)
    if data is None:
        data = getattr(result.payment_method, 'last_4', None)
        if data is None:
            data = f'UIN#{result.payment_method.customer_id}'
        else:
            data = f'Card {result.payment_method.bin}******{data}'

    if type_ == 'CreditCard':
        type_ = 'Card'
    elif type_ == 'PayPalAccount':
        type_ = 'PayPal'

    return PaymentMethodToken.objects.create(
        payment_method_token=result.payment_method.token,
        is_default=True,
        is_verified=True,
        image_url=result.payment_method.image_url,
        data=data,
        type=type_
    )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def grab_webhook(request):
    bt_signature = request.POST.get('bt_signature')
    bt_payload = request.POST.get('bt_payload')
    webhook = gateway.webhook_notification.parse(str(bt_signature), bt_payload)

    webhook_kind = webhook.kind
    subscription = webhook.subscription

    """
    braintree.WebhookNotification.Kind.SubscriptionCanceled
    braintree.WebhookNotification.Kind.SubscriptionChargedSuccessfully
    braintree.WebhookNotification.Kind.SubscriptionChargedUnsuccessfully
    braintree.WebhookNotification.Kind.SubscriptionExpired
    braintree.WebhookNotification.Kind.SubscriptionTrialEnded
    braintree.WebhookNotification.Kind.SubscriptionWentActive
    braintree.WebhookNotification.Kind.SubscriptionWentPastDue

    """
    data = {
        'balance': getattr(subscription, 'balance', None),
        'paid_through_date': getattr(subscription, 'paid_through_date', None),
        'billing_day_of_month': getattr(subscription, 'billing_day_of_month', None),
        'first_billing_date': getattr(subscription, 'first_billing_date', None),
        'billing_period_start_date': getattr(subscription, 'billing_period_start_date', None),
        'billing_period_end_date': getattr(subscription, 'billing_period_end_date', None),
        'current_billing_cycle': getattr(subscription, 'current_billing_cycle', None),
        'days_past_due': getattr(subscription, 'days_past_due', None),
        'next_billing_date': getattr(subscription, 'next_billing_date', None),
        'failure_count': getattr(subscription, 'failure_count', None),
        'bt_subscription_id': getattr(subscription, 'subscription_id', None),
        'bt_payment_method_token': getattr(subscription, 'payment_method_token', None),
        'bt_plan_id': getattr(subscription, 'plan_id', None),
        'bt_price': getattr(subscription, 'price', None),
        'bt_status': getattr(subscription, 'status', None),
        'trial_duration': getattr(subscription, 'trial_duration', None),
        'trial_duration_unit': getattr(subscription, 'trial_duration_unit', None),
        'trial_period': getattr(subscription, 'trial_period', None),
    }

    transaction = subscription.transactions[0]

    transaction_data = {
        'bt_transaction_id': getattr(transaction, 'id', None),
        'amount': getattr(transaction, 'amount', None),
        'status': getattr(transaction, 'status', None),
        'tax_amount': getattr(transaction, 'tax_amount', None),
    }

    print(data)

    status_object = None

    try:
        Subscription.objects.filter(bt_subscription_id__exact=subscription.id) \
            .update(**data)
        instance = Subscription.objects.get(subscription.id)
        status_object = instance.status
        Transaction.objects.create(
            **transaction_data,
            customer_id=instance.customer_id,
            payment_method_token_id=instance.payment_method_token_id,
            on_subscription_id=instance.id
        )
    except Exception as e:
        print(e)

    try:
        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionCanceled:
            print('SubscriptionCanceled')
            status_object.do_canceled_workflow()

        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionChargedSuccessfully:
            print('SubscriptionChargedSuccessfully')
            status_object.do_successful_workflow()

        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionChargedUnsuccessfully:
            print('SubscriptionChargedUnsuccessfully')
            status_object.do_unsuccessful_workflow()

        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionExpired:
            print('SubscriptionExpired')
            status_object.do_expired_workflow()

        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionTrialEnded:
            print('SubscriptionTrialEnded')
            status_object.do_trial_ended_workflow()

        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionWentActive:
            print('SubscriptionWentActive')
            status_object.do_activating_workflow()

        if webhook_kind == braintree.WebhookNotification.Kind.SubscriptionWentPastDue:
            print('SubscriptionWentPastDue')
            status_object.do_past_due_workflow()

    except Exception as e:
        print(e)

    return Response(status=status.HTTP_200_OK)


@login_required
def list_all_payment_methods(request):
    default_contexts = get_default_contexts(request.user)
    methods = Customer.objects.get(user_id=request.user.user_profile.id).payment_method_token.filter(is_deleted=False)
    context = {
        'methods': methods,
        'total': methods.count(),
        **default_contexts
    }
    return render(request, "payments/list_all_payment_methods.html", context=context)


@login_required
def add_default_payment_method(request):
    client_token = generate_client_token(str(request.user.user_profile.uuid))
    if request.method == "POST":
        queryset = Customer.objects.all()
        customer = get_object_or_404(queryset, uuid=request.user.user_profile.uuid)
        nonce = request.POST.get('payment_method_nonce')
        result = create_payment_method(
            customer_id=str(customer.uuid),
            payment_method_nonce=nonce,
            make_default=True
        )
        if result.is_success:
            methods = request.user.user_profile.customer.payment_method_token.filter(
                payment_method_token=result.payment_method.token
            )
            if methods.count() > 0:
                methods.update(is_default=True)
                messages.add_message(request, messages.INFO, "That payment method is now default.")
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            method = create_method(result)
            queryset: QuerySet = PaymentMethodToken.objects.filter(pk__lt=method.pk, customers__uuid=customer.uuid,
                                                                   is_deleted=False)
            queryset.update(is_default=False)
            customer.payment_method_token.add(method)
            subscription_id = customer.customer_subscription_id
            if subscription_id is not None:
                result_1 = update_subscription_payment_method(subscription_id, method.payment_method_token)
                if result_1.is_success is False:
                    delete_payment_method(method.payment_method_token)
                    method.delete()
                    return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            messages.add_message(request, messages.SUCCESS, "New payment method added!")
            request.user.user_profile.activate_the_user()
            return HttpResponseRedirect(reverse('payments:All Payment Methods'))

    return render(request, "payments/create_payment_method_first.html", {
        "client_token": client_token,
        **get_default_contexts(request.user)
    })


@login_required
def add_first_payment_method_with_registration_token(request, registration_token):
    try:
        data = signing.loads(registration_token, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
    except (signing.BadSignature, signing.SignatureExpired) as e:
        messages.add_message(request, level=messages.ERROR, message="Invalid ticket")
        request.user.user_profile.inactivate_the_user()
        logout(request)
        return HttpResponseRedirect(reverse('to_registration_platform'))

    package_uuid = data.get('package_uuid')
    try:
        package = CoursePackage.objects.get(uuid=package_uuid)
    except (CoursePackage.DoesNotExist, CoursePackage.MultipleObjectsReturned) as e:
        messages.add_message(request, level=messages.ERROR, message="Invalid file")
        request.user.user_profile.inactivate_the_user()
        logout(request)
        return HttpResponseRedirect(reverse('to_registration_platform'))

    if request.method == "POST":
        nonce = request.POST.get('payment_method_nonce')

        try:
            customer = request.user.user_profile.customer
        except (Customer.DoesNotExist, Customer.MultipleObjectsReturned) as e:
            messages.add_message(request, level=messages.ERROR,
                                 message="Please, login with a valid customer credentials")
            request.user.user_profile.inactivate_the_user()
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))

        result = create_payment_method(
            customer_id=str(customer.uuid),
            payment_method_nonce=nonce,
            make_default=True
        )
        if result.is_success:
            methods = request.user.user_profile.customer.payment_method_token.filter(
                payment_method_token=result.payment_method.token
            )
            if methods.count() > 0:
                messages.add_message(request, messages.WARNING, "That payment method already exists.")
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))

            method = create_method(result)
            queryset: QuerySet = PaymentMethodToken.objects.filter(pk__lt=method.pk, customers__uuid=customer.uuid,
                                                                   is_deleted=False)
            queryset.update(is_default=False)
            customer.payment_method_token.add(method)
            subscription_id = customer.customer_subscription_id

            if subscription_id is not None and subscription_id != "":
                result_1 = update_subscription_payment_method(subscription_id, method.payment_method_token)
                if result_1.is_success is False:
                    messages.add_message(request, messages.INFO,
                                         "You already subscribed to a course but we were unable to update to new payment method you entered.")
                    delete_payment_method(method.payment_method_token)
                    method.delete()
                    return HttpResponseRedirect(reverse('secure_accounts:Add a payment method',
                                                        kwargs={'registration_token': registration_token}))
                messages.add_message(request, messages.INFO,
                                     "You already subscribed to a course and we just updated with the new payment method you entered.")
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))

            result = create_subscription(
                payment_method_token=method.payment_method_token,
                plan_id=package.name
            )

            if result.is_success:
                user_profile = request.user.user_profile
                user_profile.package_id = package.id
                customer = user_profile.customer
                customer.customer_subscription_id = result.subscription.id
                customer.save()
                user_profile.save()
                messages.add_message(
                    request=request,
                    message='Payment method added successfully and enrolled to ' + package.name,
                    level=messages.SUCCESS
                )
                user_profile.activate_the_user()
                return HttpResponseRedirect(reverse('to_e_learning_platform'))

            messages.add_message(
                request=request,
                message='Error occurred while creating the subscription!!!',
                level=messages.ERROR
            )
            return HttpResponseRedirect(reverse('secure_accounts:Add a payment method',
                                                kwargs={'registration_token': registration_token}))

        messages.add_message(
            request=request,
            message='Error occurred while adding a new payment method!!!',
            level=messages.ERROR
        )
        return HttpResponseRedirect(reverse('secure_accounts:Add a payment method',
                                            kwargs={'registration_token': registration_token}))

    client_token = generate_client_token(str(request.user.user_profile.uuid))
    return render(request, "payments/create_payment_method_first.html", {
        "client_token": client_token,
        **get_default_contexts(request.user)
    })


@login_required
def delete_a_payment_method(request):
    queryset = Customer.objects.get(user_id=request.user.user_profile.id).payment_method_token.filter(is_deleted=False,
                                                                                                      is_verified=True)
    if request.method == "POST":
        if queryset.count() > 1:
            method = get_object_or_404(queryset, uuid=request.POST.get('id'))
            sub_id = request.user.user_profile.customer.customer_subscription_id
            if sub_id is not None and sub_id != "":
                try:
                    subs = find_subscription(sub_id)
                    if subs.payment_method_token == method.payment_method_token:
                        messages.add_message(request, messages.ERROR,
                                             "The payment method is linked with a subscription!!!")
                        return HttpResponseRedirect(reverse('payments:All Payment Methods'))
                except NotFoundError as e:
                    delete_payment_method(method.payment_method_token)
                    method.delete()
                    messages.add_message(request, messages.WARNING, "A payment method was deleted!")
                    return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            print(method.payment_method_token)
            delete_payment_method(method.payment_method_token)
            method.delete()
            messages.add_message(request, messages.WARNING, "A payment method was deleted!")
            return HttpResponseRedirect(reverse('payments:All Payment Methods'))
        messages.add_message(request, messages.WARNING, "You have to keep at lease one payment method")
        return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    context = {
        'methods': queryset,
        'total': queryset.count(),
        **get_default_contexts(request.user)
    }
    return render(request, "payments/list_all_payment_methods.html", context=context)
