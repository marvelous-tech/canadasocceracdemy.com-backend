# Generated by Django 3.1.3 on 2020-12-22 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_paymentmethodtoken_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethodtoken',
            name='type',
            field=models.CharField(blank=True, choices=[('Card', 'Card'), ('PayPal', 'PayPal')], default='Card', max_length=20, null=True),
        ),
    ]
