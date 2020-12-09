from rest_framework.serializers import ValidationError
from django.core import exceptions as django_exceptions


class PasswordMismatchError(ValidationError):
    pass


class PasswordError(django_exceptions.ValidationError):
    pass
