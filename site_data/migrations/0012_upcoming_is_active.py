# Generated by Django 3.1.3 on 2020-11-28 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_data', '0011_post_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcoming',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
