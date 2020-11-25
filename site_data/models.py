from django.db import models

from uuid import uuid4
# Create your models here.
from django.db.models.signals import pre_save

from accounts.models import Member
from mt_utils import get_logo_path, get_news_image_path, unique_slug_generator, get_gallery_image_path


class SiteData(models.Model):
    uuid = models.UUIDField(default=uuid4)
    ticket = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    page_name = models.CharField(max_length=255)
    data = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Records'

    def __str__(self):
        return f"{self.page_name} / {self.ticket}"


class Partner(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=get_logo_path)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ContactedVisitor(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=50)
    subject = models.TextField()
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ThreadReply(models.Model):
    uuid = models.UUIDField(default=uuid4)
    by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()

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

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.by


class PostCategory(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Post(models.Model):
    uuid = models.UUIDField(default=uuid4)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='newses')
    image = models.ImageField(upload_to=get_news_image_path)
    by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='newses')
    name = models.TextField(verbose_name='Title')
    sub_title = models.TextField()
    body = models.TextField()
    footer = models.TextField()
    published_at = models.DateTimeField()
    comments = models.ManyToManyField(Thread, related_name='post_comments')
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-published_at',)


class Upcoming(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.TextField(verbose_name='Title')
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='upcoming_events')
    schedule = models.DateField()
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class FAQ(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.TextField(verbose_name='Question')
    answer = models.TextField()
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Question(models.Model):
    uuid = models.UUIDField(default=uuid4)
    by = models.CharField(max_length=255)
    name = models.TextField(verbose_name='Question')
    answer = models.TextField()
    comments = models.ManyToManyField(Thread, related_name='question_comments')
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Gallery(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_gallery_image_path)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Reference(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Coupon(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Post)
pre_save.connect(pre_save_receiver, sender=Gallery)
pre_save.connect(pre_save_receiver, sender=Question)
pre_save.connect(pre_save_receiver, sender=FAQ)
pre_save.connect(pre_save_receiver, sender=Upcoming)
pre_save.connect(pre_save_receiver, sender=Partner)
pre_save.connect(pre_save_receiver, sender=Reference)
pre_save.connect(pre_save_receiver, sender=Coupon)
