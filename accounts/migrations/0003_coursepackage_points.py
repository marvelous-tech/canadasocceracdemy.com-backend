# Generated by Django 3.1.3 on 2020-12-11 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_coursepackage_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepackage',
            name='points',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
