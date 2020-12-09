from rest_framework import serializers
from email_client.models import Email


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        exclude = ('id', )
        read_only_fields = ('ein', 'user', 'message_uuid', 'message_id', 'status', 'status_code', 'error_message')
