from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from choices import USER_PROFILE_TYPE_CHOICES


class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=50)
    type = forms.ChoiceField(choices=USER_PROFILE_TYPE_CHOICES)

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'phone', 'type',
            'password1', 'password2',
        )
