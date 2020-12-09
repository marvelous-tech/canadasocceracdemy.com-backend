# Generated by Django 3.1.3 on 2020-12-02 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201202_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='has_added_data',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='has_added_payment_method',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(blank=True, choices=[('STUDENT', 'STUDENT'), ('COACH', 'COACH')], max_length=255, null=True),
        ),
    ]
