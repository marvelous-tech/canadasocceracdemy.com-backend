# Generated by Django 3.1.3 on 2020-12-28 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_data', '0016_remove_agreement_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]