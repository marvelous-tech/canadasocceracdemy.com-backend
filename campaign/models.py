import uuid

from django.db import models

# Create your models here.
from django.utils import timezone

from core.models import BaseModel


class Campaign(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CampaignPackage(BaseModel):
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='packages')

    name = models.CharField(max_length=255)
    starts = models.DateTimeField()
    ends = models.DateTimeField()

    price = models.FloatField()

    discount_percentage_off = models.FloatField(null=True, blank=True)
    discount_amount_off = models.FloatField(null=True, blank=True)

    discount_starts = models.DateTimeField(null=True, blank=True)
    discount_expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_price(self) -> float:
        if self.discount_amount_off or self.discount_percentage_off:
            today = timezone.now()
            if self.discount_starts <= today <= self.discount_expires:
                if self.discount_amount_off > 0:
                    return self.price - self.discount_amount_off
                return self.price - (self.price * self.discount_percentage_off / 100)
            # return self.price
        return self.price


class CampaignSubscriber(BaseModel):
    campaign_package = models.ForeignKey(CampaignPackage, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='subscribers')

    GENDER_CHOICES = (
        ('FEMALE', 'FEMALE'),
        ('MALE', 'MALE'),
    )

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()

    parent_names = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=255)
    parent_email = models.EmailField()
    player_email = models.EmailField()
    health_card_number = models.CharField(max_length=255)
    medications = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    injuries = models.TextField(null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=255)

    stripe_transaction = models.OneToOneField('payments.OneTimeTransaction', on_delete=models.SET_NULL, null=True,
                                              blank=True)

    def __str__(self):
        return self.name
