# Create your views here.
import stripe
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.db.models import QuerySet, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from accounts.models import CoursePackage
from core.views import get_default_contexts
from payments.gateway import *
from payments.models import Customer, PaymentMethodToken


def test_stripe(request):
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_customer_id': 'cus_Ic8EMy9x8AHVdQ'
    }
    return render(request, 'payments/add_new_payment_method.html', context=context)


@login_required
def add_default_payment_method(request):
    payload = jwt_payload_handler(request.user)
    encode = jwt_encode_handler(payload)
    # client_token = generate_client_token(str(request.user.user_profile.uuid))
    # if request.method == "POST":
    #     queryset = Customer.objects.all()
    #     customer = get_object_or_404(queryset, uuid=request.user.user_profile.uuid)
    #     nonce = request.POST.get('payment_method_nonce')
    #     result = create_payment_method(
    #         customer_id=str(customer.uuid),
    #         payment_method_nonce=nonce,
    #         make_default=True
    #     )
    #     if result.is_success:
    #         methods = request.user.user_profile.customer.payment_method_token.filter(
    #             payment_method_token=result.payment_method.token
    #         )
    #         if methods.count() > 0:
    #             methods.update(is_default=True)
    #             queryset: QuerySet = PaymentMethodToken.objects.filter(
    #                 ~Q(pk=methods.first().pk) & Q(customers__uuid=customer.uuid) & Q(is_deleted=False))
    #             queryset.update(is_default=False)
    #             messages.add_message(request, messages.INFO, "That payment method is now default.")
    #             return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #         method = create_method(result)
    #         queryset: QuerySet = PaymentMethodToken.objects.filter(
    #             ~Q(pk=method.pk) & Q(customers__uuid=customer.uuid) & Q(is_deleted=False))
    #         queryset.update(is_default=False)
    #         customer.payment_method_token.add(method)
    #         subscription_id = customer.customer_subscription_id
    #         if subscription_id is not None:
    #             result_1 = update_subscription_payment_method(subscription_id, method.payment_method_token)
    #             if result_1.is_success is False:
    #                 delete_payment_method(method.payment_method_token)
    #                 method.delete()
    #                 return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #         messages.add_message(request, messages.SUCCESS, "New payment method added!")
    #         request.user.user_profile.activate_the_user()
    #         return HttpResponseRedirect(reverse('payments:All Payment Methods'))

    context = {
        'stripe_customer_id': request.user.user_profile.customer.stripe_customer_id,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'token': encode
    }

    return render(request, "stripe_gateway/create_another_payment_method.html", {
        **context,
        **get_default_contexts(request.user)
    })


@login_required
def add_first_payment_method_with_registration_token(request, registration_token):
    payload = jwt_payload_handler(request.user)
    encode = jwt_encode_handler(payload)
    stripe.api_key = settings.STRIPE_SECRET_KEY

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

        try:
            customer = request.user.user_profile.customer
        except (Customer.DoesNotExist, Customer.MultipleObjectsReturned) as e:
            messages.add_message(request, level=messages.ERROR,
                                 message="Please, login with a valid customer credentials")
            request.user.user_profile.inactivate_the_user()
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))

        if customer.customer_subscription_id is None:
            subscription = stripe.Subscription.create(
                customer=customer.stripe_customer_id,
                items=[
                    {
                        'price': package.stripe_price_id
                    }
                ],
                expand=['latest_invoice.payment_intent']
            )
            if subscription.status == 'active':
                messages.add_message(request, level=messages.SUCCESS,
                                     message="Successfully enrolled to package " + str(package.name))
                return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
            messages.add_message(request, level=messages.ERROR,
                                 message="Failed enrolled to package " + str(package.name))
            return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
        messages.add_message(request, level=messages.INFO,
                             message="You already our user")
        return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))

    context = {
        'stripe_customer_id': request.user.user_profile.customer.stripe_customer_id,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_price_id': package.stripe_price_id,
        'registration_token': registration_token,
        'token': encode
    }
    return render(request, "stripe_gateway/create_first_payment_method.html", {
        **context,
        **get_default_contexts(request.user)
    })


@login_required
def delete_a_payment_method(request):
    queryset = Customer.objects.get(user_id=request.user.user_profile.id).payment_method_token.filter(is_deleted=False)
    if request.method == 'POST':
        if queryset.count() > 1:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer_id = request.user.user_profile.customer.stripe_customer_id
            try:
                method = queryset.get(uuid=request.POST.get('id'))
            except (PaymentMethodToken.DoesNotExist, PaymentMethodToken.MultipleObjectsReturned) as e:
                messages.add_message(request, messages.ERROR,
                                     message="That payment method does not exist")
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            if method.is_default:
                messages.add_message(request, messages.ERROR,
                                     message="You can't delete your default payment method")
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            token = method.stripe_payment_method_id
            stripe.PaymentMethod.detach(token)
            method.delete()
            stripe_customer = stripe.Customer.retrieve(customer_id)
            new_token = stripe_customer['invoice_settings']['default_payment_method']
            try:
                method = queryset.get(stripe_payment_method_id=new_token)
            except (PaymentMethodToken.DoesNotExist, PaymentMethodToken.MultipleObjectsReturned) as e:
                messages.add_message(request, messages.ERROR,
                                     message="That payment method does not exist")
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            method.is_default = True
            method.save()
            messages.add_message(request, messages.WARNING, "A payment method was deleted!")
            return HttpResponseRedirect(reverse('payments:All Payment Methods'))
        messages.add_message(request, messages.WARNING, "You have to keep at lease one payment method")
        return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    # if request.method == "POST":
    #     if queryset.count() > 1:
    #         try:
    #             method = queryset.get(uuid=request.POST.get('id'))
    #         except (PaymentMethodToken.DoesNotExist, PaymentMethodToken.MultipleObjectsReturned) as e:
    #             messages.add_message(request, messages.ERROR,
    #                                  message="That payment method does not exist")
    #             return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #         if method.is_default:
    #             messages.add_message(request, messages.ERROR,
    #                                  message="You can't delete your default payment method")
    #             return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #         sub_id = request.user.user_profile.customer.customer_subscription_id
    #         if sub_id is not None and sub_id != "":
    #             try:
    #                 subs = find_subscription(sub_id)
    #                 if subs.payment_method_token == method.payment_method_token:
    #                     messages.add_message(request, messages.ERROR,
    #                                          "The payment method is linked with a subscription!!!")
    #                     return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #             except NotFoundError as e:
    #                 delete_payment_method(method.payment_method_token)
    #                 method.delete()
    #                 messages.add_message(request, messages.WARNING, "A payment method was deleted!")
    #                 return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #         print(method.payment_method_token)
    #         delete_payment_method(method.payment_method_token)
    #         method.delete()
    #         messages.add_message(request, messages.WARNING, "A payment method was deleted!")
    #         return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    #     messages.add_message(request, messages.WARNING, "You have to keep at lease one payment method")
    #     return HttpResponseRedirect(reverse('payments:All Payment Methods'))
    context = {
        'methods': queryset,
        'total': queryset.count(),
        **get_default_contexts(request.user)
    }
    return render(request, "payments/list_all_payment_methods.html", context=context)
