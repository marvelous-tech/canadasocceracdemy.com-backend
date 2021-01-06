import json

import stripe
from django.contrib import messages
from django.db.models import Q, QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from accounts.models import CoursePackage
from mt_utils import CARD_IMAGES
from payments.models import Customer, PaymentMethodToken


def construct_data(card):
    brand = card.brand
    exp = f'{card.exp_month}/{card.exp_year}'
    funding = card.funding
    last_4 = card.last4

    data = f'{brand} {funding} ********{last_4}, EXP: {exp}'

    return data


@api_view(['POST'])
def create_first_payment_method_and_subscribe(request):
    pass


@api_view(['POST'])
def migrate_to_another_subscription(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer = request.user.user_profile.customer
    error = None
    try:
        course = CoursePackage.objects.get(uuid__exact=request.data.course)
    except Exception as e:
        course = None
        error = e

    if course is not None:
        price_id = course.stripe_price_id
        subscription = stripe.Subscription.create(
            customer=customer.stripe_customer_id,
            items=[
                {
                    'price': price_id
                }
            ],
            expand=['latest_invoice.payment_intent'],
        )
        return Response(subscription, status=status.HTTP_200_OK)
    return Response(data={'message': str(error)})


@api_view(['POST'])
def create_another_payment_method(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    data = request.data

    try:
        # Attach the payment method to the customer
        payment_method = stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=data['customerId'],
        )

        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId'],
            invoice_settings={
                'default_payment_method': data['paymentMethodId'],
            },
        )

        try:
            customer = Customer.objects.get(stripe_customer_id=data['customerId'])
        except (Customer.DoesNotExist, Customer.MultipleObjectsReturned) as e:
            customer = request.user.user_profile.customer

        if payment_method.type == 'card':
            if customer.payment_method_token.filter(payment_method_token__contains=payment_method.card.fingerprint, is_deleted=False).count() < 1:
                print("Adding new")
                token = PaymentMethodToken.objects.create(
                    payment_method_token=payment_method.card.fingerprint,
                    stripe_payment_method_id=data['paymentMethodId'],
                    type='Card',
                    image_url=CARD_IMAGES[payment_method.card.brand.upper()],
                    data=construct_data(payment_method.card),
                    is_verified=False,
                    is_default=True
                )
                customer.payment_method_token.add(token)
            else:
                messages.add_message(request, level=messages.WARNING, message="That payment method already exists")
                customer.payment_method_token.filter(
                    Q(payment_method_token__contains=payment_method.card.fingerprint)
                ).update(is_default=True)
            customer.payment_method_token.filter(
                ~Q(payment_method_token__contains=payment_method.card.fingerprint)
            ).update(is_default=False)
            print("making others non default")


        # Modify the subscription

        result = payment_method
        if customer.customer_subscription_id is not None and customer.customer_subscription_id != "":
            print("Got subscription")
            result = stripe.Subscription.modify(
                customer.customer_subscription_id,
                default_payment_method=payment_method.id
            )

        if payment_method.type == 'card':
            print(payment_method.card.fingerprint)
        print(payment_method.type)

        return Response(data={'result': result, 'redirect': reverse('payments:All Payment Methods')}, status=status.HTTP_200_OK)
    except Exception as e:
        messages.add_message(request, level=messages.ERROR, message=f"Card was declined")
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_default_api_view(request):
    customer = request.user.user_profile.customer
    method = customer.payment_method_token.filter(
        Q(uuid__exact=request.data.get('id'))
    )
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.Customer.modify(
        customer.stripe_customer_id,
        invoice_settings={
            'default_payment_method': method.first().stripe_payment_method_id,
        },
    )
    messages.add_message(request, level=messages.WARNING, message="That payment method is default now")
    method.update(is_default=True)
    customer.payment_method_token.filter(
        ~Q(uuid__exact=request.data.get('id'))
    ).update(is_default=False)
    print("making others non default")
    return Response(data={'status': 'success'}, status=status.HTTP_200_OK)
