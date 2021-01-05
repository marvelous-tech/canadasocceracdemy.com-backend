from django.contrib import admin
from stripe_gateway.models import Webhook, WebhookError

# Register your models here.


@admin.register(Webhook)
class WebhookModelAdmin(admin.ModelAdmin):
    list_display = [
        'event_type',
        'event_id',
        'created',
        'updated'
    ]


@admin.register(WebhookError)
class WebhookModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'created',
        'updated'
    ]

