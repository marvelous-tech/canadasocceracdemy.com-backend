# Generated by Django 3.1.3 on 2020-12-04 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_mockpackages_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mockpackages',
            name='amount_text',
            field=models.CharField(max_length=255),
        ),
    ]
