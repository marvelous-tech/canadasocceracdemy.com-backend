# Generated by Django 3.1.3 on 2020-12-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_data', '0010_auto_20201223_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
