# Generated by Django 4.0.4 on 2022-05-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0003_campaignsubscriber_stripe_charge_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignsubscriber',
            name='medications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignsubscriber',
            name='allergies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignsubscriber',
            name='injuries',
            field=models.TextField(blank=True, null=True),
        ),
    ]
