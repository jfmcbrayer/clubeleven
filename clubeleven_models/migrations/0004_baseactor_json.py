# Generated by Django 2.0.1 on 2018-02-28 00:25

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubeleven_models', '0003_auto_20180228_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseactor',
            name='json',
            field=django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]
