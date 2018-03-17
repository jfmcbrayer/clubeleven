# Generated by Django 2.0.1 on 2018-03-13 20:26

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubeleven_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseactor',
            name='json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='basepost',
            name='json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]
