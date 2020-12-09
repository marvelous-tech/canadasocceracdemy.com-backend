from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from django.core import exceptions as django_exceptions

from accounts.api import exceptions as mt_exceptions


class UserPasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=8, max_length=255, required=True)
    password2 = serializers.CharField(min_length=8, max_length=255, required=True)
    old_password = serializers.CharField(min_length=8, max_length=255, required=True)
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'old_password_incorrect': "The given old password was incorrect",
        'user_not_found': "Associated account not found"
    }

    class Meta:
        model = User
        fields = (
            'password1',
            'password2',
        )

    def validate_old_password(self, value):
        user = None
        try:
            user = User.objects.get(pk=self.context.get('pk'))
        except User.DoesNotExist as e:
            raise serializers.ValidationError(
                self.error_messages['user_not_found'],
                code='user_not_found',
            )
        if user:
            if user.check_password(value):
                return value
            raise serializers.ValidationError(
                self.error_messages['old_password_incorrect'],
                code='old_password_incorrect',
            )
        raise serializers.ValidationError(
            self.error_messages['user_not_found'],
            code='user_not_found',
        )

    def validate(self, attrs):
        print(attrs)
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2 and password1 != password2:
            raise mt_exceptions.PasswordMismatchError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        if password1:
            try:
                password_validation.validate_password(password1, self.instance)
            except django_exceptions.ValidationError as error:
                raise mt_exceptions.PasswordError(
                    error,
                    code='password_error',
                )

        return attrs

    def save(self, **kwargs):
        if self.is_valid():
            print(self.validated_data)
            password = self.validated_data.get('password1')
            user = None
            try:
                user = User.objects.get(pk=self.context.get('pk'))
            except User.DoesNotExist as e:
                raise serializers.ValidationError(
                    self.error_messages['user_not_found'],
                    code='user_not_found',
                )
            if user:
                user.set_password(password)
                user.save()
                user.user_profile.email_user_password_has_been_changed()
                return user
            raise serializers.ValidationError(
                self.error_messages['user_not_found'],
                code='user_not_found',
            )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserPasswordResetSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=8, max_length=255, required=True)
    password2 = serializers.CharField(min_length=8, max_length=255, required=True)

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    class Meta:
        model = User
        fields = (
            'password1',
            'password2',
        )

    def validate(self, attrs):
        print(attrs)
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        if password1:
            try:
                password_validation.validate_password(password1, self.instance)
            except serializers.ValidationError as error:
                raise serializers.ValidationError(
                    error,
                    code='password_error',
                )

        return attrs

    def save(self, **kwargs):
        if self.is_valid():
            print(self.validated_data)
            password = self.validated_data.get('password1')
            user = None
            try:
                user = User.objects.get(pk=self.context.get('pk'))
            except User.DoesNotExist as e:
                raise serializers.ValidationError(
                    self.error_messages['user_not_found'],
                    code='user_not_found',
                )
            if user:
                user.set_password(password)
                user.save()
                user.user_profile.email_user_password_has_been_reset()
                return user
            raise serializers.ValidationError(
                self.error_messages['user_not_found'],
                code='user_not_found',
            )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserCreationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, max_length=255, required=True)
    password2 = serializers.CharField(min_length=8, max_length=255, required=True)
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    phone = PhoneNumberField(required=True)
    type_ = serializers.CharField(max_length=50, required=True)
    username = serializers.EmailField(required=True)
    terms = serializers.BooleanField(required=False)

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'phone',
            'type_',
            'first_name',
            'last_name',
            'terms'
        )

    def validate(self, attrs):
        print(attrs)
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                "The two password fields didn't match.",
                code='password_mismatch',
            )

        return attrs

    def validate_password1(self, value):
        if value:
            try:
                print("password1-2")
                print(password_validation.validate_password(value, self.instance))
            except django_exceptions.ValidationError as error:
                raise serializers.ValidationError(
                    error,
                    code='password_error',
                )
            return value

    def save(self, **kwargs):
        print(self.validated_data)
        token = self.context.get('token')
        password = self.validated_data.get('password1')
        phone = self.validated_data.get('phone')
        type_ = self.validated_data.get('type_')
        user: User = User.objects.create_user(
            self.validated_data.get('username'),
            email=self.validated_data.get('username'),
            password=password,
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name')
        )
        user.refresh_from_db()
        user.user_profile.phone = phone
        user.user_profile.type = type_
        user.save()
        user.user_profile.email_user_activation_code_with_registration_token(registration_token=token)
        return user
