from django.urls import path, include

from payments.views import list_all_payment_methods, \
    add_default_payment_method, \
    delete_a_payment_method

from stripe_gateway.views import add_default_payment_method, delete_a_payment_method

app_name = "payments"

urlpatterns = [
    path("all/", list_all_payment_methods, name="All Payment Methods"),
    path("create/", add_default_payment_method, name="Add Payment Method"),
    path("delete/", delete_a_payment_method, name="Delete Payment Method"),
]
