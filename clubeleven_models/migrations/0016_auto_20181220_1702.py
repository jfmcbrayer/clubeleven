# Generated by Django 2.1.4 on 2018-12-20 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubeleven_models', '0015_auto_20181220_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baseactor',
            old_name='type',
            new_name='ap_type',
        ),
    ]