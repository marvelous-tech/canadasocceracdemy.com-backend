# Generated by Django 3.1.3 on 2021-01-04 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_coursepackage_stripe_price_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursepackage',
            options={'ordering': ['id']},
        ),
    ]
