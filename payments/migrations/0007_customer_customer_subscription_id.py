# Generated by Django 3.1.3 on 2020-12-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20201204_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
