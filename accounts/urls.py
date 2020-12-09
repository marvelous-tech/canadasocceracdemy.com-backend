from django.urls import path, include, re_path

from accounts.views import secure_login, login_user, logout_user, enroll, migrate, cancel_subscriptions, \
    verify_email_with_registration_code
from payments.views import add_first_payment_method_with_registration_token

app_name = "secure_accounts"

urlpatterns = [
    path('login-prompt/<str:token>/', secure_login, name="Login to secure account"),
    path('login/', login_user, name="Login to your account"),
    path('logout/', logout_user, name="Logging out"),
    path('enroll/<str:token>/', enroll, name="Enroll"),
    path('migrate/<str:token>/', migrate, name="Migrate"),
    path('subscriptions/', cancel_subscriptions, name="cancel_subscriptions"),
    path('first-verify-email/<str:code>/', verify_email_with_registration_code, name="Verifying your email"),
    path('first-method/<str:registration_token>/', add_first_payment_method_with_registration_token,
         name="Add a payment method")
]
