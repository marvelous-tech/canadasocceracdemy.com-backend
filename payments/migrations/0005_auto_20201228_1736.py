# Generated by Django 3.1.3 on 2020-12-28 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20201222_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethodtoken',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
    ]
