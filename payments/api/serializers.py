from rest_framework import serializers

from payments.models import PaymentMethodToken


class PaymentMethodTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethodToken
        fields = [
            'uuid',
            'name',
            'image_url',
            'bin',
            'card_last_digits',
            'cardholder_name',
            'expiration_month',
            'expiration_year',
            'is_verified',
            'is_default'
        ]
