from uuid import uuid4

from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404
from private_storage.fields import PrivateFileField

from accounts.models import UserProfile, Member, CoursePackage, User
from comment.models import Thread
from e_learning.fields import VideoField
from mt_utils import unique_slug_generator, get_course_video_thumbnail_path, get_course_video_path, \
    get_course_video_cc_path


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid4)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_comments', blank=True, null=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_comments', blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uuid


class CourseCategory(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    description_box = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CourseVideoMark(models.Model):
    uuid = models.UUIDField(default=uuid4)
    time = models.FloatField(default=0)
    note = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)


class CourseVideoQueryset(models.QuerySet):
    def queryset(self) -> models.QuerySet:
        return self.select_related('category', 'package').prefetch_related('comments', 'marks', 'instructors__user')

    @staticmethod
    def get_course_videos_by_package_points(queryset, package_points) -> models.QuerySet:
        return queryset.filter(package__points__lte=package_points, is_deleted=False).order_by('-id')

    @staticmethod
    def get_course_videos_by_package_points_by_category_id(queryset, package_points, category_id) -> models.QuerySet:
        return CourseVideoQueryset.get_course_videos_by_package_points(queryset, package_points).filter(category_id=category_id).order_by('-id')

    @staticmethod
    def get_course_video_by_package_points_by_category_id_by_slug(queryset, package_points, category_id, course_video_slug):
        return get_object_or_404(
            CourseVideoQueryset.get_course_videos_by_package_points_by_category_id(queryset, package_points, category_id), slug=course_video_slug)


class CourseVideo(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255, verbose_name='Title')
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    description_box = models.TextField(blank=True, null=True)
    video = VideoField(upload_to=get_course_video_path, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_course_video_thumbnail_path, blank=True, null=True)
    cc = models.FileField(upload_to=get_course_video_cc_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        CourseCategory, on_delete=models.CASCADE, related_name='course_videos', blank=True, null=True)
    package = models.ForeignKey(
        CoursePackage, on_delete=models.CASCADE, related_name='course_videos', blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name='course_video_comments')
    marks = models.ManyToManyField(CourseVideoMark, blank=True, related_name='course_videos')
    instructors = models.ManyToManyField(Member, blank=True, related_name='course_videos')
    slug = models.SlugField(blank=True, null=True, max_length=255)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CourseVideoQueryset.as_manager()

    def __str__(self):
        return self.name


class CoursePlaylistQuerySet(models.QuerySet):
    def queryset(self) -> models.QuerySet:
        return self.prefetch_related(
            'videos__comments', 'videos__marks', 'videos__instructors', 'videos__category', 'videos__package')

    @staticmethod
    def get_playlists_by_package_points(queryset, package_points):
        return queryset.filter(videos__package__points__lte=package_points).order_by('-id')

    @staticmethod
    def get_playlist_by_package_points_by_slug(queryset, package_points, playlist_slug):
        return get_object_or_404(CoursePlaylistQuerySet.get_playlists_by_package_points(queryset, package_points), slug=playlist_slug)


class CoursePlaylist(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=255)
    description_box = models.TextField(blank=True, null=True)
    videos = models.ManyToManyField(CourseVideo, related_name='playlists', blank=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CoursePlaylistQuerySet.as_manager()

    def __str__(self):
        return self.name


class WatchLetterPlaylist(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='watch_letter_videos')
    videos = models.ManyToManyField(CourseVideo, blank=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CoursePlaylistQuerySet.as_manager()

    def __str__(self):
        return self.uuid


class CourseVideoHistory(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='course_video_history')
    course_video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE, related_name='views')
    at_time = models.FloatField(default=0.0)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.uuid)


class ThumbUpUserVideo(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='thumb_up_videos')
    course_video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE, related_name='thumb_ups')
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.uuid


def pre_save_receiver_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver_slug, sender=CourseCategory)
pre_save.connect(pre_save_receiver_slug, sender=CoursePlaylist)
pre_save.connect(pre_save_receiver_slug, sender=CourseVideo)
