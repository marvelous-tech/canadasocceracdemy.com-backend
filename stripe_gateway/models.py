from django.db import models

# Create your models here.


class Webhook(models.Model):
    event_id = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_type


class WebhookError(models.Model):
    error_data = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
