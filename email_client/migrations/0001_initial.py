# Generated by Django 3.1.3 on 2020-12-14 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import email_client.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.PositiveBigIntegerField(auto_created=True, blank=True, editable=False, null=True)),
                ('message_uuid', models.UUIDField(auto_created=True, blank=True, editable=False, null=True)),
                ('ein', models.PositiveBigIntegerField(auto_created=True, default=email_client.models.create_ein, editable=False)),
                ('from_email', models.EmailField(max_length=254)),
                ('from_name', models.CharField(max_length=255)),
                ('to_email', models.EmailField(max_length=254)),
                ('to_name', models.CharField(max_length=255)),
                ('subject', models.TextField()),
                ('text_body', models.TextField()),
                ('html_body', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('status_code', models.PositiveSmallIntegerField(default=200)),
                ('error_message', models.TextField(blank=True, default='', null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
