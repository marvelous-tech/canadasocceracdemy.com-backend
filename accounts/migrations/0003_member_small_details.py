# Generated by Django 3.1.3 on 2020-12-22 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201222_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='small_details',
            field=models.TextField(null=True),
        ),
    ]
