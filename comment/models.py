from uuid import uuid4

from django.db import models

# Create your models here.
from accounts.models import Member


class ThreadReply(models.Model):
    uuid = models.UUIDField(default=uuid4)
    by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.by


class Thread(models.Model):
    uuid = models.UUIDField(default=uuid4)
    by = models.CharField(max_length=255)
    body = models.TextField()
    replies = models.ManyToManyField(ThreadReply, related_name='comments')
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.by
