from django.urls import path, include

from stripe_gateway.api.views import create_another_payment_method, make_default_api_view, attempt_adding_payment_method
from stripe_gateway.api.webhook_views import webhook_capture

app_name = 'STRIPE_INTEGRATIONS_CORE_API'

urlpatterns = [
    path('create-another-payment-method/', create_another_payment_method, name="CREATE_ANOTHER_PAYMENT_METHOD_API"),
    path('webhook/', webhook_capture),
    path('make-default/', make_default_api_view, name="MAKE_DEFAULT_API_VIEW"),
    path('attempt/', attempt_adding_payment_method, name="ATTEMPT")
]
