# Generated by Django 3.1.3 on 2020-11-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0006_auto_20201130_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='courseplaylist',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]