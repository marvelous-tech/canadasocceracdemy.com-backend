from django.contrib import admin

# Register your models here.
from payments.models import PaymentMethodToken, \
    Customer, \
    Subscription, \
    SubscriptionStatus, \
    Transaction


@admin.register(PaymentMethodToken)
class PaymentMethodTokenModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'payment_method_token',
        'type',
        'data',
        'is_verified',
        'is_default',
        'is_deleted',
        'created',
        'updated'
    ]


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'uuid',
        'payment_method_token',
        'is_deleted',
        'created',
        'updated',
    ]
    search_fields = ['stripe_customer_id', ]


@admin.register(Subscription)
class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'customer',
        'payment_method_token',
        'plan_id',
        'is_deleted',
        'created',
        'updated'
    ]


@admin.register(SubscriptionStatus)
class SubscriptionStatusModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'is_in_trial',
        'status',
        'subscription',
        'was_charged_successfully',
        'is_deleted',
        'created',
        'updated'
    ]


@admin.register(Transaction)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'customer',
        'payment_method_token',
        'on_subscription',
        'was_success',
        'is_deleted',
        'created',
        'updated'
    ]
