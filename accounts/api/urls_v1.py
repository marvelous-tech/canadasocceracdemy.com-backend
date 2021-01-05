from django.urls import path, re_path, include

from accounts.api.views import \
    SignUpUserCreateAPIView, \
    verify_email_api_view, \
    get_password_reset_code, \
    password_reset_api_view, \
    password_change_api_view, \
    get_default_data, enroll_api_view, migrate_package_api_view, check_is_valid_to_enroll, check_has_any_subscriptions, \
    generate_registration_token, signup_api_view, check_email_is_unique, check_phone_number

app_name = 'accounts'

urlpatterns = [
    path('check_email/<str:email>/', check_email_is_unique, name="check_email_is_unique"),
    path('check_phone/<str:number>/', check_phone_number, name="check_phone_number"),
    path('get_registration_file/<uuid:package_uuid>/', generate_registration_token, name="generate_registration_token"),
    path('signup/<str:token>/', signup_api_view, name="signup_api_view"),
    path('activate/<str:uidb64>/<str:token>/',
         verify_email_api_view, name="activate_account"),
    path('get-reset-code/<str:email>/', get_password_reset_code, name="get_password_reset_code"),
    path('reset/<str:code>/',
         password_reset_api_view, name="password_reset_api_view"),
    path('change-password/', password_change_api_view, name="password_change_api_view"),
    path('data/', get_default_data, name="get_default_data"),
    path('enrollment/', include([
        path('enroll/<uuid:package_uuid>/', enroll_api_view, name="enroll_api_view"),
        path('migrate/<uuid:package_uuid>/', migrate_package_api_view, name="migrate_package_api_view"),
        path('check_valid/', check_is_valid_to_enroll, name="check_is_valid_to_enroll"),
        path('has_any_subs/', check_has_any_subscriptions, name="check_has_any_subscriptions"),
    ]))
]
