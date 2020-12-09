# Generated by Django 3.1.3 on 2020-12-08 06:32

from django.db import migrations
import mt_utils
import private_storage.fields
import private_storage.storage.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0009_courseplaylist_description_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursevideo',
            name='video',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.s3boto3.PrivateS3BotoStorage(), upload_to=mt_utils.get_course_video_path),
        ),
    ]
