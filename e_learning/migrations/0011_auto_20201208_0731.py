# Generated by Django 3.1.3 on 2020-12-08 07:31

from django.db import migrations
import e_learning.fields
import mt_utils


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0010_auto_20201208_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursevideo',
            name='video',
            field=e_learning.fields.VideoField(upload_to=mt_utils.get_course_video_path),
        ),
    ]
