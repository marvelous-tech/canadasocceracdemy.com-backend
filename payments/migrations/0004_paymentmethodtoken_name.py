# Generated by Django 3.1.3 on 2020-12-04 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_customer_was_created_successfully'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethodtoken',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
