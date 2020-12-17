from rest_framework import serializers

from payments.models import PaymentMethodToken


class PaymentMethodTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethodToken
        fields = [
            'uuid',
            'type',
            'data',
            'image_url',
            'is_verified',
            'is_default'
        ]
