# Generated by Django 3.1.2 on 2020-10-25 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_client', '0002_auto_20201025_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='message_id',
            field=models.PositiveBigIntegerField(auto_created=True, blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='message_uuid',
            field=models.UUIDField(auto_created=True, blank=True, editable=False, null=True),
        ),
    ]
