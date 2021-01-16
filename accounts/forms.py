from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile
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


class ChangeUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, min_length=2)
    last_name = forms.CharField(required=True, min_length=1)
    email = forms.EmailField(required=True, min_length=4)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]


class ChangeProfilePicture(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'profile_image'
        ]
