import os
import json

import requests
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from email_client.api.serializers import EmailSerializer
from email_client.models import Email


class EmailCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Email.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            return self.create(request, *args, **kwargs)
        return Response({"details": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        if serializer.is_valid():
            headers = {'Content-Type': 'application/json'}
            email = requests.post(
                'https://api.mailjet.com/v3.1/send',
                auth=(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS')),
                data=json.dumps({
                    "Messages": [
                        {
                            "From": {
                                "Email": serializer.validated_data["from_email"],
                                "Name": serializer.validated_data["from_name"]
                            },
                            "To": [
                                {
                                    "Email": serializer.validated_data["to_email"],
                                    "Name": serializer.validated_data["to_name"]
                                }
                            ],
                            "Subject": serializer.validated_data["subject"],
                            "TextPart": serializer.validated_data["text_body"],
                            "HTMLPart": serializer.validated_data["html_body"]
                        }
                    ]
                }),
                headers=headers
            )
            data = email.json()
            print(data)
            if email.status_code == 200:
                to = data["Messages"][0]["To"][0]
                serializer.save(user_id=self.request.user.id, message_uuid=to["MessageUUID"], message_id=to["MessageID"],
                                status=True)
            else:
                serializer.save(user_id=self.request.user.id, status=False, status_code=email.status_code, error_message=data["ErrorMessage"])
