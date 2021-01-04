from uuid import uuid4

import stripe
from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from accounts.models import UserProfile, CoursePackage
from choices import SUBSCRIPTION_STATUS_CHOICES, SubscriptionStatusName
from payments import gateway


class PaymentMethodToken(models.Model):
    uuid = models.UUIDField(default=uuid4, verbose_name='Token ID')
    payment_method_token = models.CharField(max_length=100, help_text="Fingerprint for Stripe")
    type = models.CharField(max_length=20, choices=(
        ('Card', 'Card'),
        ('PayPal', 'PayPal')
    ), default='Card', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    data = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    stripe_payment_method_id = models.CharField(max_length=255, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.uuid)


class Customer(models.Model):
    uuid = models.UUIDField(default=uuid4, verbose_name='Customer ID')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='customer')
    payment_method_token = models.ManyToManyField(PaymentMethodToken, related_name='customers', blank=True)
    is_deleted = models.BooleanField(default=False)
    was_created_successfully = models.BooleanField(default=False)
    customer_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    clear_till = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Stripe
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    last_payment_has_error = models.BooleanField(default=False)
    last_payment_error_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.uuid)


class Subscription(models.Model):
    uuid = models.UUIDField(default=uuid4)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='subscription')
    payment_method_token = models.OneToOneField(PaymentMethodToken, on_delete=models.CASCADE, related_name='subscription')
    plan_id = models.ForeignKey(CoursePackage, on_delete=models.CASCADE, related_name='subscriptions')

    balance = models.FloatField(blank=True, null=True)
    paid_through_date = models.DateField(blank=True, null=True)
    billing_day_of_month = models.PositiveSmallIntegerField(blank=True, null=True)
    first_billing_date = models.DateField(blank=True, null=True)
    billing_period_start_date = models.DateField(blank=True, null=True)
    billing_period_end_date = models.DateField(blank=True, null=True)
    current_billing_cycle = models.PositiveIntegerField(blank=True, null=True)
    days_past_due = models.PositiveIntegerField(blank=True, null=True)
    next_billing_date = models.DateField(blank=True, null=True)

    failure_count = models.PositiveSmallIntegerField(blank=True, null=True)

    bt_subscription_id = models.CharField(max_length=255, verbose_name='Subscription ID', blank=True, null=True)
    bt_payment_method_token = models.CharField(max_length=255, blank=True, null=True)
    bt_plan_id = models.CharField(max_length=255, blank=True, null=True)
    bt_price = models.FloatField(blank=True, null=True)
    bt_status = models.CharField(max_length=50, blank=True, null=True)

    trial_duration = models.PositiveSmallIntegerField(blank=True, null=True)
    trial_duration_unit = models.CharField(max_length=5, blank=True, null=True)
    trial_period = models.BooleanField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)


class SubscriptionStatus(models.Model):
    uuid = models.UUIDField(default=uuid4, verbose_name='Subscription Status ID')
    is_in_trial = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE, related_name='status')
    was_charged_successfully = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

    def do_unsuccessful_workflow(self):
        self.subscription.customer.user.inactivate_the_user()
        self.was_charged_successfully = SubscriptionStatusName.UNSUCCESSFUL
        self.save()

    def do_past_due_workflow(self):
        self.subscription.customer.user.inactivate_the_user()
        self.status = SubscriptionStatusName.PAST_DUE
        self.save()

    def do_canceled_workflow(self):
        self.subscription.customer.user.inactivate_the_user()
        self.status = SubscriptionStatusName.CANCELED
        self.save()

    def do_expired_workflow(self):
        self.subscription.customer.user.expire_the_user()
        self.status = SubscriptionStatusName.EXPIRED
        self.save()

    def do_trial_ended_workflow(self):
        if self.is_in_trial is True:
            self.is_in_trial = SubscriptionStatusName.NOT_IN_TRIAL
            self.is_in_trial = False
            self.save()

    def do_activating_workflow(self):
        self.subscription.customer.user.activate_the_user()
        self.is_in_trial = SubscriptionStatusName.ACTIVE
        self.save()

    def do_successful_workflow(self):
        self.was_charged_successfully = SubscriptionStatusName.SUCCESSFUL
        self.save()


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid4)
    bt_transaction_id = models.CharField(max_length=255, verbose_name='Transaction ID', blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    payment_method_token = models.ForeignKey(PaymentMethodToken, on_delete=models.CASCADE, related_name='transactions')
    on_subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='transactions')
    was_success = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    tax_amount = models.FloatField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.uuid)


@receiver(post_save, sender=UserProfile)
def update_user_profile(sender, instance: UserProfile, created, **kwargs):
    if created:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            customer = stripe.Customer.create(
                name=instance.user.first_name + ' ' + instance.user.last_name,
                email=instance.user.email,
                phone=instance.phone,
                metadata={'uuid': instance.uuid, 'type': instance.get_type_display()}
            )
            # result = gateway.create_new_customer(
            #     customer_id=str(instance.uuid),
            #     first_name=instance.user.first_name,
            #     last_name=instance.user.last_name,
            #     email=instance.user.email,
            #     phone=instance.phone
            # )
            Customer.objects.create(
                user_id=instance.id,
                uuid=instance.uuid,
                was_created_successfully=True,
                stripe_customer_id=customer.id
            )
        except Exception as e:
            pass
    instance.customer.save()
