from django.db import models

from uuid import uuid4
# Create your models here.
from django.db.models.signals import pre_save
from tinymce.models import HTMLField

from accounts.models import Member
from comment.models import Thread
from mt_utils import get_logo_path, get_news_image_path, unique_slug_generator, get_gallery_image_path, get_image_path, \
    get_agreement_image_path, get_camp_image_path


class SiteLogo(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_logo_path)
    for_content = models.CharField(max_length=50)
    style = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class SiteData(models.Model):
    uuid = models.UUIDField(default=uuid4)
    ticket = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    page_name = models.CharField(max_length=255)
    data = HTMLField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Site Content Data'

    def __str__(self):
        return f"{self.page_name} / {self.ticket}"


class BannerImage(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_image_path)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Partner(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=get_logo_path)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ContactedVisitor(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    subject = models.TextField(null=True, blank=True)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


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
    name = models.TextField(verbose_name="Title", null=True, blank=True)
    sub_title = models.TextField(null=True, blank=True)
    body = HTMLField(null=True, blank=True)
    footer = HTMLField(null=True, blank=True)
    published_at = models.DateTimeField()
    comments = models.ManyToManyField(Thread, related_name='post_comments', blank=True)
    is_active = models.BooleanField(default=True)
    tags = models.TextField(blank=True, null=True)
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
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class FAQ(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.TextField(verbose_name='Question')
    answer = HTMLField()
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

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
    is_feature = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class GalleryVideo(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    youtube_video_id = models.CharField(max_length=255)
    is_feature = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

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


class Testimonial(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default="")
    text = HTMLField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Address(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.CharField(max_length=255)
    address = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ContactNumber(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Email(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.CharField(max_length=255)
    email = models.EmailField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Agreement(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.TextField()
    agreement_image = models.ImageField(upload_to=get_agreement_image_path)
    text = HTMLField(blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class TermAndCondition(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.TextField()
    text = HTMLField()
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class PrivacyPolicy(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.TextField()
    text = HTMLField()
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class CampImage(models.Model):
    uuid = models.UUIDField(default=uuid4)

    image = models.ImageField(upload_to=get_camp_image_path)
    name = models.TextField()
    text = HTMLField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Camp(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.TextField()
    text = HTMLField()
    flyer_image = models.ImageField(upload_to=get_camp_image_path, null=True)
    images = models.ManyToManyField(CampImage, related_name='camps', blank=True)
    timestamp = models.DateTimeField(null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    uuid = models.UUIDField(default=uuid4)

    name = models.TextField()
    link = models.URLField()
    logo = models.ImageField(upload_to=get_logo_path)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


def pre_save_receiver_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver_slug, sender=Post)
pre_save.connect(pre_save_receiver_slug, sender=Gallery)
pre_save.connect(pre_save_receiver_slug, sender=GalleryVideo)
pre_save.connect(pre_save_receiver_slug, sender=Question)
pre_save.connect(pre_save_receiver_slug, sender=FAQ)
pre_save.connect(pre_save_receiver_slug, sender=Upcoming)
pre_save.connect(pre_save_receiver_slug, sender=Partner)
pre_save.connect(pre_save_receiver_slug, sender=Reference)
pre_save.connect(pre_save_receiver_slug, sender=Coupon)
pre_save.connect(pre_save_receiver_slug, sender=Agreement)
pre_save.connect(pre_save_receiver_slug, sender=TermAndCondition)
pre_save.connect(pre_save_receiver_slug, sender=PrivacyPolicy)
pre_save.connect(pre_save_receiver_slug, sender=Camp)
