# Generated by Django 3.1.3 on 2021-01-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_gateway', '0002_auto_20210124_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='is_succeed',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
    ]
