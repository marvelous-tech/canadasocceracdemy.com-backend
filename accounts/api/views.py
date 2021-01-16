from django.contrib.auth.models import User
from django.core import signing
from django.db.models import QuerySet, Q
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.conf import settings
import phonenumbers

from accounts.api.exceptions import PasswordError, PasswordMismatchError
from accounts.api.serializers import UserCreationSerializer, UserPasswordResetSerializer, UserPasswordChangeSerializer
from accounts.api.tokens import account_activation_token
from accounts.models import CoursePackage, UserProfile
from payments import gateway
from payments.models import PaymentMethodToken

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_default_data(request):
    user = request.user
    user_profile = user.user_profile
    if bool(user_profile.profile_image) is False:
        profile_image = None
    else:
        profile_image = user_profile.profile_image.url
    data = {
        'email': user.email,
        'phone': user_profile.phone.as_international,
        'name': f'{user.first_name} {user.last_name}',
        'type': user_profile.type,
        'profile_image': profile_image,
        'valid': user_profile.is_active is True and user_profile.is_deleted is False and user_profile.is_expired is False and user_profile.email_verified is True
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])  # TODO: add urls
def get_password_reset_code(request, email):
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as e:
        return Response({'error_msg': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    if user:
        user.user_profile.email_user_password_reset_code()
        return Response({'success': "A password reset code has been sent to your email"}, status=status.HTTP_200_OK)
    return Response({'error_msg': "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])  # TODO: add urls
def password_change_api_view(request):
    serializer = UserPasswordChangeSerializer(data=request.data, context={
        'pk': request.user.pk
    })
    if serializer.is_valid():
        serializer.save()
        payload = jwt_payload_handler(request.user)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'user': payload}, status=status.HTTP_201_CREATED)
    return Response({'error_msg': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])  # TODO: add urls
def password_reset_api_view(request, code):
    try:
        data = signing.loads(code, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
    except (signing.BadSignature, signing.SignatureExpired) as e:
        return Response({"token_error": True, "error": "Invalid ticket"})
    uidb64 = data.get('uidb64')
    token = data.get('token')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={
            'pk': user.pk
        })
        if serializer.is_valid():
            serializer.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token, 'user': payload}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error_msg': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error_msg': 'Invalid token or Expired!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup_api_view(request, token):
    try:
        data = signing.loads(token, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
    except (signing.BadSignature, signing.SignatureExpired) as e:
        return Response({"token_error": True, "error": "Invalid ticket"})

    package_uuid = data.get('package_uuid')
    try:
        CoursePackage.objects.get(uuid=package_uuid)
    except (CoursePackage.DoesNotExist, CoursePackage.MultipleObjectsReturned) as e:
        return Response({"token_error": True, "error": "Invalid File"})

    if User.objects.filter(username=request.data.get('username')).count() > 0:
        return Response({"user_error": "Email already taken."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserCreationSerializer(data=request.data, context={"token": token})

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({**serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SignUpUserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserCreationSerializer


@api_view(['GET'])
@permission_classes([AllowAny, ])  # TODO: add urls
def verify_email_api_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.user_profile.is_active = True
        user.user_profile.email_verified = True
        user.save()
        user.user_profile.email_user_account_activated()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'user': payload}, status=status.HTTP_200_OK)
    else:
        return Response({'error_msg': 'Invalid token or Expired!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def enroll_api_view(request, package_uuid):
    if request.user.user_profile.customer.customer_subscription_id is None:
        try:
            customer_uuid = request.user.user_profile.uuid
        except UserProfile.DoesNotExist as e:
            return Response({'signup_error': 'signup properly'}, status=status.HTTP_404_NOT_FOUND)
        try:
            package = CoursePackage.objects.get(uuid=package_uuid)
        except CoursePackage.DoesNotExist as e:
            return Response({'package_error': 'Package Not found'}, status=status.HTTP_404_NOT_FOUND)
        default_payment_method: QuerySet = PaymentMethodToken.objects.prefetch_related('customers').filter(
            customers__uuid=customer_uuid,
            is_default=True,
            is_deleted=False
        )
        if default_payment_method.count() < 1:
            return Response({'payment_method_error': 'No Payment method found!'}, status=status.HTTP_404_NOT_FOUND)
        token = default_payment_method.first().payment_method_token
        result = gateway.create_subscription(
            payment_method_token=token,
            plan_id=package.name
        )
        if result.is_success:
            user_profile = request.user.user_profile
            user_profile.package_id = package.id
            customer = user_profile.customer
            customer.customer_subscription_id = result.subscription.id
            customer.save()
            user_profile.save()
            return Response({'enrolled': 'Successfully enrolled to ' + package.name}
                            , status=status.HTTP_201_CREATED)
        return Response({'subscription_error': 'Error occurred while creating the subscription!!!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'subscription_exists': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def migrate_package_api_view(request, package_uuid):
    if request.user.user_profile.customer.customer_subscription_id is not None:
        try:
            user_profile = request.user.user_profile
            customer_uuid = user_profile.uuid
        except UserProfile.DoesNotExist as e:
            return Response({'signup_error': 'signup properly'}, status=status.HTTP_404_NOT_FOUND)
        try:
            package = CoursePackage.objects.get(uuid=package_uuid)
        except CoursePackage.DoesNotExist as e:
            return Response({'package_error': 'Package Not found'}, status=status.HTTP_404_NOT_FOUND)
        default_payment_method: QuerySet = PaymentMethodToken.objects.prefetch_related('customers').filter(
            customers__uuid=customer_uuid,
            is_default=True,
            is_deleted=False
        )
        if default_payment_method.count() < 1:
            return Response({'payment_method_error': 'No Payment method found!'}, status=status.HTTP_404_NOT_FOUND)
        subscription_id = user_profile.customer.customer_subscription_id
        if subscription_id is None:
            return Response({'no_subscriptions': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)
        result = gateway.update_subscription(
            subscription_id=subscription_id,
            plan_id=package.name
        )
        if result.is_success:
            user_profile.package_id = package.id
            user_profile.save()
            return Response({'migrated': 'Successfully migrated to ' + package.name}
                            , status=status.HTTP_201_CREATED)
        return Response({'subscription_error': 'Error occurred while upgrading the subscription!!!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'subscription_not_found': 'Must subscribe to a course'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_is_valid_to_enroll(request):
    customer = request.user.user_profile.customer
    if customer.payment_method_token.filter(is_deleted=False, is_verified=True).count() > 0\
            and request.user.user_profile.email_verified \
            and request.user.user_profile.is_active \
            and request.user.user_profile.is_deleted is False \
            and request.user.user_profile.is_expired is False:
        return Response({'status': True}, status=status.HTTP_200_OK)
    return Response({'status': False}, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_has_any_subscriptions(request):
    customer = request.user.user_profile.customer
    if customer.customer_subscription_id is not None and customer.customer_subscription_id != "":
        return Response({'status': True}, status=status.HTTP_200_OK)
    return Response({'status': False}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def generate_registration_token(request, package_uuid):
    try:
        CoursePackage.objects.get(uuid=package_uuid)
    except CoursePackage.DoesNotExist as e:
        return Response({"error_msg": "Package not found"}, status=status.HTTP_404_NOT_FOUND)
    msg = {
        'package_uuid': str(package_uuid),
    }
    value = signing.dumps(msg)
    return Response({'file': value}, status=status.HTTP_200_OK)

"""
http://127.0.0.1:8000/secure/first-verify-email/eyJ1aWRiNjQiOiJNelkiLCJ0b2tlbiI6ImFla3RvNi1iNDMxYzEzMDAyOTQ4NTc1MmQxYTgxNmU3ODEyZDI5NSIsInJlZ2lzdHJhdGlvbl90b2tlbiI6ImV5SndZV05yWVdkbFgzVjFhV1FpT2lJelltUTBaR0l4TkMxaU1UUXlMVFJqWXpBdFlUUXhNaTAzTUdGbE9UTTFNR0kyWTJVaWZROjFrbWVpbzo2ekVjQ290emZMTmxxWVdEVm4xMkxhaTY5NDBjRGFKa2xDdGNicUlzWHk0In0:1kmiW6:uC3kxQHPfErT499hEg1A04WeH8zbrvAHNMYKyy2cmac/
"""


@api_view(['GET'])
@permission_classes([AllowAny, ])
def check_email_is_unique(request, email):
    try:
        user = User.objects.get(Q(username=email) | Q(email=email))
        if user:
            return Response({'error': True}, status=status.HTTP_200_OK)
    except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
        return Response({'error': False}, status=status.HTTP_200_OK)
    return Response({'server_error': True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def check_phone_number(request, number):
    try:
        x = phonenumbers.parse(number)
        print(x)
    except Exception as e:
        return Response({"phone_error": True}, status=status.HTTP_200_OK)
    return Response({"phone_error": False}, status=status.HTTP_200_OK)
