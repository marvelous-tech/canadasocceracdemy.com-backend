# Generated by Django 3.1.3 on 2020-12-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20201202_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='was_created_successfully',
            field=models.BooleanField(default=False),
        ),
    ]