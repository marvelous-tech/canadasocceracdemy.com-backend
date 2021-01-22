from django.contrib import admin

# Register your models here.
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

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
        'get_payment_methods',
        'is_attempt',
        'is_deleted',
        'created',
        'updated',
    ]
    search_fields = ['stripe_customer_id', 'uuid']
    readonly_fields = ['payment_method_token', 'user']

    def get_queryset(self, request):
        qs: QuerySet = super(CustomerModelAdmin, self).get_queryset(request)
        return qs.select_related('user__user').prefetch_related('payment_method_token')

    @staticmethod
    def get_payment_methods(obj):
        data = "\n"

        for p in obj.obj.payment_method_token.all():
            data += "<p>"
            data += f"{p.data} stripe={p.stripe_payment_method_id} "
            if p.is_verified:
                data += "<span>"
                data += "<img width='13px' src='https://marvelous-tech.nyc3.cdn.digitaloceanspaces.com/check.svg'/>"
                data += "</span>"
            else:
                data += "<span>"
                data += "<img width='13px' src='https://marvelous-tech.nyc3.cdn.digitaloceanspaces.com/delete.svg'/>"
                data += "</span>"

        data = mark_safe(data)
        return data


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
