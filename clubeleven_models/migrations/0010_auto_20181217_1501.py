# Generated by Django 2.1.4 on 2018-12-17 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubeleven_models', '0009_inspectablemessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectablemessage',
            name='json',
            field=models.TextField(blank=True, null=True),
        ),
    ]
