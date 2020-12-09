from django.urls import path, include, re_path

from payments.api.views import get_client_token_api_view, add_default_payment_method_api_view, \
    list_all_payment_methods_api_view, delete_payment_method_api_view, generate_token

app_name = "payments_api"

urlpatterns = [
    path('client/', include([
        path('token/', get_client_token_api_view, name="get_client_token_api_view"),
    ])),
    path('method/', include([
        path('all/', list_all_payment_methods_api_view, name="list_all_payment_methods_api_view"),
        path('add/', add_default_payment_method_api_view, name="add_default_payment_method_api_view"),
        path('delete/', delete_payment_method_api_view, name="delete_payment_method_api_view"),
        path('get_file/<str:type_>/<uuid:package_uuid>/', generate_token, name="generate_token"),
        path('get_file/<str:type_>/<str:package_uuid>/', generate_token, name="generate_token"),
    ])),
]
