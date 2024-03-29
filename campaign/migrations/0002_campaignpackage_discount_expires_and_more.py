# Generated by Django 4.0.4 on 2022-05-29 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignpackage',
            name='discount_expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campaignpackage',
            name='discount_starts',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignpackage',
            name='discount_amount_off',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignpackage',
            name='discount_percentage_off',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
