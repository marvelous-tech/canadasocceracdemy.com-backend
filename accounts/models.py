from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from choices import MEMBER_TYPE_CHOICES

User = get_user_model()

# Create your models here.


class Member(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    phone = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, choices=MEMBER_TYPE_CHOICES)

    def __str__(self):
        return self.user.name

