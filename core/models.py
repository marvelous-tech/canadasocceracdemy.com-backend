import uuid

from django.db import models

# Create your models here.


def get_guid():
    return uuid.uuid4().hex


class BaseModel(models.Model):
    guid = models.CharField(max_length=255, default=get_guid, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
