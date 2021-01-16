import datetime
from datetime import timedelta
from django.utils.timezone import now

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core import signing

import json

# Create your views here.
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from accounts.api.tokens import account_activation_token
from accounts.forms import ChangeUserProfileForm, ChangeProfilePicture
from accounts.models import CoursePackage, UserProfile
from payments import gateway
from payments.models import PaymentMethodToken


def home_registration(request, *args, **kwargs):
    logout(request)
    return render(request, 'accounts/home.html')


def password_reset_email_entry_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if email is None:
            messages.add_message(request, messages.ERROR, "Please, give your email")
            return HttpResponseRedirect(reverse('secure_accounts:reset_password_email_entry'))
        try:
            user = User.objects.get(email=email)
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            user = None

        if user is not None:
            print("user got")
            if user.email:
                print("user email got")
                user.user_profile.email_user_password_reset_code()

        messages.add_message(request, messages.SUCCESS, f"Password reset url has been sent to {email}")
        return HttpResponseRedirect(reverse('secure_accounts:reset_password_email_entry'))

    return render(request, 'accounts/password-reset-email-entry.html', {})


def password_reset_view(request, code):
    try:
        data = signing.loads(code, max_age=datetime.timedelta(seconds=3600))
    except (signing.BadSignature, signing.SignatureExpired) as e:
        messages.add_message(request, messages.ERROR, "Invalid signature, typically it is valid 5 minutes.")
        return HttpResponseRedirect(reverse('secure_accounts:reset_password'))

    uidb64 = data.get('uidb64')
    token = data.get('token')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.add_message(request, messages.ERROR, "Invalid user, typically it is valid 5 minutes.")
        return HttpResponseRedirect(reverse('secure_accounts:reset_password'))

    if request.method == 'POST':
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password_confirm', None)

        if password and password_confirm and password == password_confirm:
            if user is not None and account_activation_token.check_token(user, token):
                user.set_password(password)
                user.save()
                user.user_profile.email_user_password_has_been_reset()
                messages.add_message(request, messages.WARNING, "Your password has been reset")
                return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))

            messages.add_message(request, messages.ERROR, "User validation failed, typically it is valid 5 minutes.")
            return HttpResponseRedirect(reverse('secure_accounts:reset_password'))

        messages.add_message(request, messages.ERROR, "Please, fill-up the form")
        return HttpResponseRedirect(reverse('secure_accounts:reset_password'))

    return render(request, 'accounts/password-reset.html', {})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(settings.E_LEARNING_PLATFORM)
    if request.method == 'POST':
        raw_password = request.POST.get('password')
        username = request.POST.get('email')
        auth_user = authenticate(request, username=username, password=raw_password)
        if auth_user is not None:
            login(request, user=auth_user)
            messages.add_message(
                request=request,
                message="Logged in successfully",
                level=messages.SUCCESS
            )
            if request.user.is_superuser:
                return redirect('/admin')
            next_ = request.GET.get('next', settings.E_LEARNING_PLATFORM)
            return redirect(next_)
        messages.add_message(
            request=request,
            message="Incorrect password",
            level=messages.ERROR
        )
        return render(request, template_name='accounts/main-login.html', context={
            'fetal_error': False
        })
    return render(request, template_name='accounts/main-login.html', context={
        'fetal_error': False
    })


def secure_login(request, token):
    logout(request)
    try:
        data = signing.loads(token, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
    except signing.SignatureExpired as e:
        messages.add_message(
            request=request,
            message="Expired file",
            level=messages.ERROR
        )
        return render(request, template_name='accounts/login.html', context={
            'fetal_error': True
        })
    except signing.BadSignature as e:
        messages.add_message(
            request=request,
            message="Invalid file",
            level=messages.ERROR
        )
        return render(request, template_name='accounts/login.html', context={
            'fetal_error': True
        })

    user_id = data.get('user_id')
    package_uuid = data.get('package_uuid')
    type_ = data.get('type')

    try:
        user = User.objects.get(pk=int(user_id))
    except User.DoesNotExist as e:
        messages.add_message(
            request=request,
            message="No User found",
            level=messages.ERROR
        )
        return render(request, template_name='accounts/login.html', context={
            'fetal_error': True
        })

    try:
        package = CoursePackage.objects.get(uuid=package_uuid)
    except CoursePackage.DoesNotExist as e:
        messages.add_message(
            request=request,
            message="No Package found",
            level=messages.ERROR
        )
        return render(request, template_name='accounts/login.html', context={'user': user, 'fetal_error': False})


    if request.method == 'POST':
        raw_password = request.POST.get('password')
        print(raw_password)
        auth_user = authenticate(username=user.username, password=raw_password)
        if auth_user is not None:
            login(request, user=auth_user)
            messages.add_message(
                request=request,
                message="Logged in successfully",
                level=messages.SUCCESS
            )
            if type_ == 'enroll':
                return HttpResponseRedirect(reverse('secure_accounts:Enroll', kwargs={
                    'token': token
                }))
            if type_ == 'billing':
                return HttpResponseRedirect(reverse('payments:All Payment Methods'))
            if type_ == 'migrate':
                return HttpResponseRedirect(reverse('secure_accounts:Migrate', kwargs={
                        'token': token
                }))
            messages.add_message(
                request=request,
                message="Invalid file",
                level=messages.ERROR
            )
            return render(request, template_name='accounts/login.html', context={
                'fetal_error': True
            })
        messages.add_message(
            request=request,
            message="Incorrect password",
            level=messages.ERROR
        )
        return render(request, template_name='accounts/login.html', context={
            'user': user, 'fetal_error': False
        })
    return render(request, template_name='accounts/login.html', context={
        'user': user, 'fetal_error': False
    })


@login_required
def enroll(request, token):
    try:
        data = signing.loads(token, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
    except signing.SignatureExpired as e:
        messages.add_message(
            request=request,
            message="Expired file",
            level=messages.ERROR
        )
        logout(request)
        return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
    except signing.BadSignature as e:
        messages.add_message(
            request=request,
            message="Invalid file",
            level=messages.ERROR
        )
        logout(request)
        return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
    # user_id = data.get('user_id')
    package_uuid = data.get('package_uuid')

    if request.user.user_profile.customer.customer_subscription_id is None or request.user.user_profile.customer.customer_subscription_id == "":
        try:
            customer_uuid = request.user.user_profile.uuid
        except UserProfile.DoesNotExist as e:
            messages.add_message(
                request=request,
                message="No User found",
                level=messages.ERROR
            )
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
        try:
            package = CoursePackage.objects.get(uuid=package_uuid)
        except CoursePackage.DoesNotExist as e:
            messages.add_message(
                request=request,
                message="No Package found",
                level=messages.ERROR
            )
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
        default_payment_method: QuerySet = PaymentMethodToken.objects.prefetch_related('customers').filter(
            customers__uuid=customer_uuid,
            is_default=True,
            is_deleted=False
        )
        if default_payment_method.count() < 1:
            messages.add_message(
                request=request,
                message="Please add at least one valid payment method",
                level=messages.ERROR
            )
            return HttpResponseRedirect(reverse('payments:Add Payment Method'))
        if request.method == "POST":
            result = True
            print(result)
            if result:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                subscription = stripe.Subscription.create(
                    customer=request.user.user_profile.customer.stripe_customer_id,
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
            messages.add_message(
                request=request,
                message='Error occurred while creating the subscription!!!',
                level=messages.WARNING
            )
            return HttpResponseRedirect(reverse('payments:All Payment Methods'))
        return render(request, 'accounts/enroll.html', {
            'package': package
        })
    print(request.user.user_profile.package.uuid)
    print(package_uuid)
    if str(request.user.user_profile.package.uuid) == package_uuid:
        messages.add_message(
            request=request,
            message='Already subscribed to this package',
            level=messages.INFO
        )
        return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
    messages.add_message(
        request=request,
        message='Already subscribed',
        level=messages.INFO
    )
    return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))


@login_required
def migrate(request, token):
    try:
        data = signing.loads(token, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
    except signing.SignatureExpired as e:
        messages.add_message(
            request=request,
            message="Expired file",
            level=messages.ERROR
        )
        logout(request)
        return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
    except signing.BadSignature as e:
        messages.add_message(
            request=request,
            message="Invalid file",
            level=messages.ERROR
        )
        logout(request)
        return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
    # user_id = data.get('user_id')
    package_uuid = data.get('package_uuid')

    if request.user.user_profile.customer.customer_subscription_id is not None and request.user.user_profile.customer.customer_subscription_id != "":

        if str(request.user.user_profile.package.uuid) == package_uuid:
            messages.add_message(
                request=request,
                message='Already subscribed to this package',
                level=messages.INFO
            )
            return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))

        try:
            customer_uuid = request.user.user_profile.uuid
        except UserProfile.DoesNotExist as e:
            messages.add_message(
                request=request,
                message="No User found",
                level=messages.ERROR
            )
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))

        try:
            package = CoursePackage.objects.get(uuid=package_uuid)
        except CoursePackage.DoesNotExist as e:
            messages.add_message(
                request=request,
                message="No Package found",
                level=messages.ERROR
            )
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
        default_payment_method: QuerySet = PaymentMethodToken.objects.prefetch_related('customers').filter(
            customers__uuid=customer_uuid,
            is_default=True,
            is_deleted=False
        )
        if default_payment_method.count() < 1:
            messages.add_message(
                request=request,
                message="Please add at least one valid payment method",
                level=messages.ERROR
            )
            return HttpResponseRedirect(reverse('payments:Add Payment Method'))
        if request.method == "POST":
            user_profile = request.user.user_profile
            subscription_id = user_profile.customer.customer_subscription_id
            if subscription_id is None:
                messages.add_message(
                    request=request,
                    message='No previous subscription found',
                    level=messages.WARNING
                )
                return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
            result = gateway.update_subscription(
                subscription_id=subscription_id,
                plan_id=package.name
            )
            if result.is_success:
                user_profile.package_id = package.id
                user_profile.save()
                messages.add_message(
                    request=request,
                    message='Successfully migrated to ' + package.name,
                    level=messages.SUCCESS
                )
                return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
            messages.add_message(
                request=request,
                message='Error occurred while migrating the subscription!!!',
                level=messages.WARNING
            )
            return HttpResponseRedirect(reverse('payments:All Payment Methods'))
        return render(request, 'accounts/migrate.html', {
            'package': package
        })
    messages.add_message(
        request=request,
        message='Must be subscribed to a course',
        level=messages.ERROR
    )
    return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))


@login_required
def cancel_subscriptions(request):
    package = request.user.user_profile.package
    customer = request.user.user_profile.customer
    subscription_id = customer.customer_subscription_id
    if customer.clear_till:
        if customer.clear_till <= now():
            if subscription_id is not None:
                try:
                    stripe.Subscription.delete(subscription_id)
                except Exception as e:
                    print(e)
                    customer.customer_subscription_id = None
                    customer.was_created_successfully = True
                    customer.last_payment_has_error = False
                    customer.last_payment_error_comment = None
                    customer.clear_till = None
                    customer.user.package_id = None
                    customer.user.save()
                    customer.cancel_scheduled = False
                    customer.save()
                    pass

    if request.method == "POST":
        if subscription_id is None:
            messages.add_message(
                request=request,
                message='No previous subscription found',
                level=messages.WARNING
            )
            return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
        result = True  # gateway.cancel_subscription(subscription_id=subscription_id)
        if result:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            customer = request.user.user_profile.customer
            customer.cancel_scheduled = True
            messages.add_message(
                request=request,
                message=f'The subscription has been scheduled to cancel at {customer.clear_till.ctime()}',
                level=messages.WARNING
            )
            return HttpResponseRedirect(reverse('secure_accounts:cancel_subscriptions'))
        else:
            messages.add_message(
                request=request,
                message='Error while canceling the subscription',
                level=messages.ERROR
            )
    return render(request, 'accounts/subscribed_package.html', {
        'package': package,
        'customer': customer,
        'clear': customer.clear_till >= now() if customer.clear_till else False
    })


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))


def verify_email_with_registration_code(request, code):
    try:
        print("m")
        data = signing.loads(code, max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
        print("m")
        uid = force_text(urlsafe_base64_decode(data.get('uidb64')))
        print("m")
        token = data.get('token')
        print("m")
        registration_data = signing.loads(data.get('registration_token'), max_age=settings.TOKEN_EXPIRATION_TIMEDELTA)
        print("m")
    except (signing.BadSignature, signing.SignatureExpired) as e:
        messages.add_message(request, level=messages.ERROR, message="Invalid Link. Typically these links are valid for 1 day.")
        return HttpResponseRedirect(reverse('to_registration_platform'))

    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, User.MultipleObjectsReturned):
        messages.add_message(request, level=messages.ERROR, message="Invalid identification. Typically these links are valid for 1 day.")
        return HttpResponseRedirect(reverse('to_registration_platform'))

    if user is not None:
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.user_profile.activate_the_user()
            user.user_profile.email_verified = True
            user.user_profile.save()
            user.save()
            user.user_profile.email_user_account_activated()
            logout(request)
            return HttpResponseRedirect(reverse('secure_accounts:Add a payment method', kwargs={'registration_token': data.get('registration_token')}))

    messages.add_message(request, level=messages.ERROR, message="Invalid ticket. Typically these links are valid for 1 day.")
    return HttpResponseRedirect(reverse('to_registration_platform'))


def change_user_profile_view(request):
    if request.method == 'POST':
        form = ChangeUserProfileForm(data=request.POST, instance=request.user)
        form.save()


def change_user_profile_image(request):
    if request.method == 'POST':
        form = ChangeProfilePicture(files=request.FILES, data=request.POST, instance=request.user.user_profile)
        form.save()
