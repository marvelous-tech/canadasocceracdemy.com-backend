from uuid import uuid4

import stripe
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import signing
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from accounts.api.tokens import account_activation_token
from choices import MEMBER_TYPE_CHOICES, USER_PROFILE_TYPE_CHOICES, CYCLE_TYPE_CHOICES
from email_client.api.serializers import EmailSerializer
from mt_utils import get_profile_image_path, unique_slug_generator, email, get_package_feature_image_path


# Create your models here.
# from payments import gateway


class Member(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member', blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=MEMBER_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    details = HTMLField(null=True)
    small_details = models.TextField(null=True)

    objects = models.Manager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class CoursePackage(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0)
    description_box = HTMLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    cycle = models.CharField(max_length=50, choices=CYCLE_TYPE_CHOICES, default="MONTHLY")
    image = models.ImageField(upload_to=get_package_feature_image_path, blank=True, null=True)
    points = models.PositiveSmallIntegerField(default=0)
    currency = models.CharField(max_length=3, choices=(('CAD', 'CAD'), ('USD', 'USD')), default='USD')
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    stripe_price_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class MockPackages(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    amount_text = models.CharField(max_length=255)
    description_box = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to=get_package_feature_image_path, null=True)
    packages = models.ManyToManyField(CoursePackage, related_name='mocks', blank=True)
    currency = models.CharField(max_length=3, choices=(('CAD', 'CAD'), ('USD', 'USD')), default='USD')
    is_monthly = models.BooleanField(null=True)
    is_annually = models.BooleanField(null=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE, related_name='user_profiles', blank=True, null=True)
    type = models.CharField(max_length=255, choices=USER_PROFILE_TYPE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    has_added_data = models.BooleanField(default=False)
    has_added_payment_method = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def expire_the_user(self):
        if self.is_expired is False:
            self.is_expired = True
            self.is_active = False
            self.save()

    def activate_the_user(self):
        if self.is_active is False:
            self.is_active = True
            self.is_expired = False
            self.is_deleted = False
            self.save()

    def inactivate_the_user(self):
        if self.is_active is True:
            self.is_active = False
            self.save()

    def delete_the_user_profile(self):
        if self.is_deleted is False:
            self.is_deleted = True
            self.is_active = False
            self.is_expired = True
            self.save()

    def email_user_subscription_scheduled(self, cancel_at):
        link = f'{settings.SERVER}/dashboard/subscriptions/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Subscription Scheduled Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name} [{self.package.name}] [UTC {cancel_at.ctime()}]',
            'subject': f'Subscription Package {self.package.name} Scheduled to Cancel at UTC {cancel_at.ctime()}',
            'text_body': f'Your subscription for {self.package.name} was scheduled to cancel at UTC {cancel_at.ctime()} for {self.user.email}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': f'Your subscription for {self.package.name} was scheduled to cancel at {cancel_at.ctime()} for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_subscription_deleted(self, timestamp):
        link = f'{settings.SERVER}/dashboard/subscriptions/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Subscription Canceled Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': f'Subscription Canceled [{self.package.name}] [UTC {timestamp.ctime()}]',
            'text_body': f'Your subscription for {self.package.name} was canceled at UTC {timestamp.ctime()} for {self.user.email}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': f'Your subscription for {self.package.name} was canceled at {timestamp.ctime()} for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_payment_failed(self, card_data, timestamp, error_msg):
        link = f'{settings.SERVER}/dashboard/payments/all/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Payment Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': f'Payment Failed',
            'text_body': f'{error_msg} Your payment with {card_data} was Failed at UTC {timestamp.ctime()} for {self.user.email}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': f'{error_msg} Your payment with {card_data} was failed at UTC {timestamp.ctime()} for',
                'button_text': 'GO TO YOUR BILLING'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_card_declined(self, card_data, timestamp, error_msg):
        link = f'{settings.SERVER}/dashboard/payments/all/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Payment Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': f'Card Declined [{card_data}] [UTC {timestamp.ctime()}]',
            'text_body': f'{error_msg} Your {card_data} was DECLINED at UTC {timestamp.ctime()} for {self.user.email}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': f'{error_msg} Your {card_data} was DECLINED at UTC {timestamp.ctime()} for',
                'button_text': 'GO TO YOUR BILLING'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_subscription_success(self):
        link = f'{settings.SERVER}/to-elearning-platform/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Subscription Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': f'Subscription Package {str(self.package.name)} Valid till [UTC {self.customer.clear_till.ctime()}]',
            'text_body': f'Subscribing to package {str(self.package.name)} was successful and will renew at UTC {self.customer.clear_till.ctime()} for {self.user.email}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': f'Subscribing to package {str(self.package.name)} was successful and will renew at UTC {self.customer.clear_till.ctime()} for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_payment_succeeded(self, card_data, timestamp, trx_id):
        link = f'{settings.SERVER}/to-elearning-platform/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Payment Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': f'Payment Succeeded for {str(self.package.name)} TRX_ID: #{trx_id} [{card_data}] [UTC {timestamp.ctime()}]',
            'text_body': f'Your payment with {card_data} was successfully done at UTC {timestamp.ctime()} for {self.user.email}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': f'Your payment with {card_data} was successfully done at UTC {timestamp.ctime()} for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_activation_code(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        link = f'{settings.SERVER}/secure/activate/{uid}/{token}/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Email Verification Code Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': 'Verify your email to activate account',
            'text_body': f'Activate your account here {link}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': 'Please click on the button to complete the verification process for',
                'button_text': 'VERIFY YOUR EMAIL ADDRESS'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_activation_code_with_registration_token(self, registration_token):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        code = signing.dumps({
            'uidb64': uidb64,
            'token': token,
            'registration_token': registration_token
        })
        link = f'{settings.SERVER}/secure/first-verify-email/{code}/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Email Verification Code Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': 'Verify your email to activate account',
            'text_body': f'Activate your account here {link}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': 'Please click on the button to complete the verification process for',
                'button_text': 'VERIFY YOUR EMAIL ADDRESS'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_account_activated(self):
        link = f'{settings.SERVER}/to-elearning-platform/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Account Activated Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': 'Your account has been activated',
            'text_body': f'Your account has been activated. Now add payment method. Your account here {link}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': 'Your account has been activated. Now add payment method for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_password_reset_code(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        code = signing.dumps({
            'uidb64': uid,
            'token': token
        })
        link = f'{settings.SERVER}/secure/password/reset/{code}/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Password Reset Code Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': 'Account password reset code',
            'text_body': f'Reset your password here {link}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': 'Please click on the button to complete the password reset process for',
                'button_text': 'RESET YOUR PASSWORD'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_password_has_been_reset(self):
        link = f'{settings.SERVER}/secure/login/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Password Reset Notification Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': 'Account password has been reset',
            'text_body': f'Your password has been reset. Go to your account {link}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': 'Your password has been reset for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)

    def email_user_password_has_been_changed(self):
        link = f'{settings.SERVER}/secure/login/'
        serializer = EmailSerializer(data={
            'from_email': settings.NO_REPLY_MAIL_ADDRESS,
            'from_name': 'Password Changed Canadasocceracademy.com',
            'to_email': self.user.email,
            'to_name': f'{self.user.first_name} {self.user.last_name}',
            'subject': 'Account password was changed',
            'text_body': f'Your account password was changed. Go to your account {link}',
            'html_body': render_to_string('email_client/account_notification_template.html', {
                'link': link,
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email,
                'company': 'Canadasocceracademy.com',
                'company_phone': settings.SUPPORT_PHONE_NUMBER,
                'company_support_email': settings.SUPPORT_MAIL_ADDRESS,
                'msg': 'Your password was changed for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print("Attempt to Sending email")
        email(serializer, self.user_id)


def pre_save_receiver_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver_slug, sender=CoursePackage)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user_id=instance.id)
    instance.user_profile.save()


@receiver(pre_delete, sender=User)
def user_auto_unsubscribe(sender, instance, using, **kwargs):
    try:
        customer_id = instance.user_profile.customer.stripe_customer_id
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.Customer.delete(customer_id)
    except Exception as e:
        print(e)
        pass
