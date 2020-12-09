from django.urls import path
from email_client.api.views import EmailCreateAPIView

app_name = 'email_api'

urlpatterns = [
    path('send/', EmailCreateAPIView.as_view(), name='email_create_api_view'),
]
