# Generated by Django 3.1.3 on 2021-01-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_auto_20210102_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cancel_scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
