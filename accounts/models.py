from uuid import uuid4

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
from payments import gateway


class Member(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member', blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=MEMBER_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

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
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MockPackages(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    amount_text = models.CharField(max_length=255)
    description_box = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to=get_package_feature_image_path, null=True)
    packages = models.ManyToManyField(CoursePackage, related_name='mocks', blank=True)
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

    def email_user_activation_code(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        link = f'{settings.SERVER}/secure/activate/{uid}/{token}/'
        serializer = EmailSerializer(data={
            'from_email': 'customers@marvelous-tech.com',
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
                'company_phone': '+880 1632 77-6159',
                'company_support_email': 'support@marvelous-tech.com',
                'msg': 'Please click on the button to complete the verification process for',
                'button_text': 'VERIFY YOUR EMAIL ADDRESS'
            })
        })
        print(serializer)
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
            'from_email': 'customers@marvelous-tech.com',
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
                'company_phone': '+880 1632 77-6159',
                'company_support_email': 'support@marvelous-tech.com',
                'msg': 'Please click on the button to complete the verification process for',
                'button_text': 'VERIFY YOUR EMAIL ADDRESS'
            })
        })
        print(serializer)
        email(serializer, self.user_id)

    def email_user_account_activated(self):
        link = f'{settings.SERVER}/to-elearning-platform/'
        serializer = EmailSerializer(data={
            'from_email': 'customers@marvelous-tech.com',
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
                'company_phone': '+880 1632 77-6159',
                'company_support_email': 'support@marvelous-tech.com',
                'msg': 'Your account has been activated. Now add payment method for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print(serializer)
        email(serializer, self.user_id)

    def email_user_password_reset_code(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        link = f'{settings.SERVER}/secure/password/reset/{uid}/{token}/'
        serializer = EmailSerializer(data={
            'from_email': 'customers@marvelous-tech.com',
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
                'company_phone': '+880 1632 77-6159',
                'company_support_email': 'support@marvelous-tech.com',
                'msg': 'Please click on the button to complete the password reset process for',
                'button_text': 'RESET YOUR PASSWORD'
            })
        })
        print(serializer)
        email(serializer, self.user_id)

    def email_user_password_has_been_reset(self):
        link = f'{settings.SERVER}/secure/'
        serializer = EmailSerializer(data={
            'from_email': 'customers@marvelous-tech.com',
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
                'company_phone': '+880 1632 77-6159',
                'company_support_email': 'support@marvelous-tech.com',
                'msg': 'Your password has been reset for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print(serializer)
        email(serializer, self.user_id)

    def email_user_password_has_been_changed(self):
        link = f'{settings.SERVER}/secure/'
        serializer = EmailSerializer(data={
            'from_email': 'customers@marvelous-tech.com',
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
                'company_phone': '+880 1632 77-6159',
                'company_support_email': 'support@marvelous-tech.com',
                'msg': 'Your password was changed for',
                'button_text': 'GO TO YOUR ACCOUNT'
            })
        })
        print(serializer)
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
        subscription_id = instance.user_profile.customer.customer_subscription_id
        if subscription_id is None or subscription_id == "":
            pass
        else:
            result = gateway.cancel_subscription(subscription_id=subscription_id)
            if result.is_success:
                user_profile = instance.user_profile
                user_profile.package = None
                user_profile.save()
                customer = user_profile.customer
                customer.customer_subscription_id = None
                customer.save()
            else:
                pass
    except User.DoesNotExist as e:
        pass
