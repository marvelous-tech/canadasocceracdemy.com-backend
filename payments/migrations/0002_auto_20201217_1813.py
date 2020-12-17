# Generated by Django 3.1.3 on 2020-12-17 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethodtoken',
            name='bin',
        ),
        migrations.RemoveField(
            model_name='paymentmethodtoken',
            name='card_last_digits',
        ),
        migrations.RemoveField(
            model_name='paymentmethodtoken',
            name='cardholder_name',
        ),
        migrations.RemoveField(
            model_name='paymentmethodtoken',
            name='expiration_month',
        ),
        migrations.RemoveField(
            model_name='paymentmethodtoken',
            name='expiration_year',
        ),
        migrations.RemoveField(
            model_name='paymentmethodtoken',
            name='name',
        ),
        migrations.AddField(
            model_name='paymentmethodtoken',
            name='data',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
