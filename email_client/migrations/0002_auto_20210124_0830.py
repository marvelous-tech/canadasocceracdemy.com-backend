# Generated by Django 3.1.3 on 2021-01-24 08:30

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('email_client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='html_body',
            field=tinymce.models.HTMLField(),
        ),
    ]
