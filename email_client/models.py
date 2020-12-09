from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now

from mt_utils import create_hash


def create_ein():
    return int(create_hash("Contract" + str(now())), 16) % (10 ** 12)


class Email(models.Model):
    ein = models.PositiveBigIntegerField(editable=False, auto_created=True, default=create_ein)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='emails')

    from_email = models.EmailField()
    from_name = models.CharField(max_length=255)

    to_email = models.EmailField()
    to_name = models.CharField(max_length=255)

    subject = models.TextField()
    text_body = models.TextField()
    html_body = models.TextField()

    message_uuid = models.UUIDField(auto_created=True, editable=False, null=True, blank=True)
    message_id = models.PositiveBigIntegerField(auto_created=True, editable=False, null=True, blank=True)

    status = models.BooleanField(default=False)
    status_code = models.PositiveSmallIntegerField(default=200)

    error_message = models.TextField(default="", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.from_email
