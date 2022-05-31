# Generated by Django 3.1.3 on 2022-05-31 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_onetimetransaction'),
        ('campaign', '0006_merge_20220531_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignsubscriber',
            name='stripe_charge_id',
        ),
        migrations.AddField(
            model_name='campaignsubscriber',
            name='stripe_transaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.onetimetransaction'),
        ),
    ]
