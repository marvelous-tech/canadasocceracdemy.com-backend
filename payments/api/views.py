# Create your views here.
import json
from datetime import datetime, timedelta

from braintree.exceptions import NotFoundError
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.core import signing

from accounts.models import CoursePackage
from payments.api.serializers import PaymentMethodTokenSerializer
from payments.gateway import *
from payments.models import Customer, PaymentMethodToken


@api_view(['GET'])
def get_client_token_api_view(request):
    return Response({
        'client_token': generate_client_token(str(
            request.user.user_profile.uuid
        ))
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_all_payment_methods_api_view(request):
    methods = Customer.objects.get(user_id=request.user.user_profile.id).payment_method_token.filter(is_deleted=False)
    serializer = PaymentMethodTokenSerializer(instance=methods, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_default_payment_method_api_view(request):
    queryset = Customer.objects.all()
    customer = get_object_or_404(queryset, uuid=request.user.user_profile.uuid)
    nonce = request.data.get('payment_method_nonce')
    result = create_payment_method(
        customer_id=str(customer.uuid),
        payment_method_nonce=nonce,
        make_default=True
    )
    tokens = PaymentMethodToken.objects.filter(payment_method_token=result.payment_method.token, is_deleted=False)
    if tokens.count() > 0:
        return Response({'already_exist': True}, status=status.HTTP_400_BAD_REQUEST)
    print(result)
    if result.is_success:
        method = PaymentMethodToken.objects.create(
            payment_method_token=result.payment_method.token,
            is_default=True,
            is_verified=True,
            name=result.payment_method.card_type,
            bin=result.payment_method.bin,
            card_last_digits=result.payment_method.last_4,
            image_url=result.payment_method.image_url,
            cardholder_name=result.payment_method.cardholder_name,
            expiration_month=result.payment_method.expiration_month,
            expiration_year=result.payment_method.expiration_year,
        )
        queryset: QuerySet = PaymentMethodToken.objects.filter(pk__lt=method.pk, customers__uuid=customer.uuid, is_deleted=False)
        queryset.update(is_default=False)
        customer.payment_method_token.add(method)
        subscription_id = customer.customer_subscription_id
        if subscription_id is not None:
            result_1 = update_subscription_payment_method(subscription_id, method.payment_method_token)
            if result_1.is_success is False:
                delete_payment_method(method.payment_method_token)
                method.delete()
                return Response({'subscription_error': True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'added': True}, status=status.HTTP_201_CREATED)
    return Response({'payment_method_error': True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def delete_payment_method_api_view(request):
    found = False
    queryset = Customer.objects.get(user_id=request.user.user_profile.id).payment_method_token.filter(is_deleted=False, is_verified=True)
    if queryset.count() > 1:
        method = get_object_or_404(queryset, uuid=request.data.get('id'))
        try:
            subscription_id = request.user.user_profile.customer.customer_subscription_id
            if subscription_id is not None:
                find_subscription(subscription_id)
                found = True
        except NotFoundError as e:
            found = False
        if found is False:
            delete_payment_method(method.payment_method_token)
            method.delete()
            return Response({'deleted': True}, status=status.HTTP_200_OK)
    return Response({'deleted': False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def generate_token(request, type_, package_uuid):
    if package_uuid != 'dispatch':
        try:
            CoursePackage.objects.get(uuid=package_uuid)
        except CoursePackage.DoesNotExist as e:
            return Response({"error_msg": "Package not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        package_uuid = CoursePackage.objects.all().first().uuid
    user = request.user.id
    msg = {
        'user_id': user,
        'package_uuid': str(package_uuid),
        'type': type_
    }
    value = signing.dumps(msg)
    return Response({'file': value}, status=status.HTTP_200_OK)
