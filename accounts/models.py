from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save

from choices import MEMBER_TYPE_CHOICES, USER_PROFILE_TYPE_CHOICES
from mt_utils import get_profile_image_path, unique_slug_generator

User = get_user_model()

# Create your models here.


class Member(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    phone = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, choices=MEMBER_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)

    def __str__(self):
        return self.user.username


class CoursePackage(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0)
    description_box = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone = models.CharField(max_length=255, blank=True, null=True)
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE, related_name='user_profiles', blank=True, null=True)
    type = models.CharField(max_length=255, choices=USER_PROFILE_TYPE_CHOICES)

    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)

    def __str__(self):
        return self.user.username


def pre_save_receiver_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver_slug, sender=CoursePackage)
