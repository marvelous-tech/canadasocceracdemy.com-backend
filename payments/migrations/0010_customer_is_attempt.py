# Generated by Django 3.1.3 on 2021-01-22 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_customer_cancel_scheduled'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_attempt',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
