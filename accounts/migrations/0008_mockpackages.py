# Generated by Django 3.1.3 on 2020-12-04 19:04

from django.db import migrations, models
import mt_utils
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_coursepackage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockPackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('amount_text', models.CharField(max_length=5)),
                ('description_box', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(null=True, upload_to=mt_utils.get_package_feature_image_path)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
