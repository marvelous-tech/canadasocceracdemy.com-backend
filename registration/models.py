from uuid import uuid4

from django.db import models

# Create your models here.
from site_data.models import Camp


class CampRegistration(models.Model):
    uuid = models.UUIDField(default=uuid4)

    camp = models.ForeignKey(Camp, on_delete=models.SET_NULL, related_name='registrations', null=True)

    objects = models.Manager()

    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
