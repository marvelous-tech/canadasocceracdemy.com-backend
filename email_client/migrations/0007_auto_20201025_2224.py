# Generated by Django 3.1.2 on 2020-10-25 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_client', '0006_auto_20201025_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='from_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='to_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]