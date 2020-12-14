# Generated by Django 3.1.3 on 2020-12-11 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import e_learning.fields
import mt_utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('message', models.TextField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_comments', to=settings.AUTH_USER_MODEL)),
                ('to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('description_box', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('sub_title', models.CharField(blank=True, max_length=255, null=True)),
                ('description_box', models.TextField(blank=True, null=True)),
                ('video', e_learning.fields.VideoField(blank=True, null=True, upload_to=mt_utils.get_course_video_path)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=mt_utils.get_course_video_thumbnail_path)),
                ('cc', models.FileField(blank=True, null=True, upload_to=mt_utils.get_course_video_cc_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_videos', to='e_learning.coursecategory')),
                ('comments', models.ManyToManyField(blank=True, related_name='course_video_comments', to='e_learning.Comment')),
                ('instructors', models.ManyToManyField(blank=True, related_name='course_videos', to='accounts.Member')),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideoMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('time', models.FloatField(default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WatchLetterPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='watch_letter_videos', to='accounts.userprofile')),
                ('videos', models.ManyToManyField(blank=True, to='e_learning.CourseVideo')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbUpUserVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('course_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumb_ups', to='e_learning.coursevideo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumb_up_videos', to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideoHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('at_time', models.FloatField(default=0.0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('course_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='e_learning.coursevideo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_video_history', to='accounts.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='marks',
            field=models.ManyToManyField(blank=True, related_name='course_videos', to='e_learning.CourseVideoMark'),
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_videos', to='accounts.coursepackage'),
        ),
        migrations.CreateModel(
            name='CoursePlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('description_box', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('videos', models.ManyToManyField(blank=True, related_name='playlists', to='e_learning.CourseVideo')),
            ],
        ),
    ]
