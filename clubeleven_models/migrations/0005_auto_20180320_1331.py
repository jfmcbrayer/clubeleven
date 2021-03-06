# Generated by Django 2.0.1 on 2018-03-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubeleven_models', '0004_auto_20180320_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='follows',
        ),
        migrations.AddField(
            model_name='baseactor',
            name='followers',
            field=models.ManyToManyField(related_name='_baseactor_followers_+', to='clubeleven_models.BaseActor'),
        ),
        migrations.AddField(
            model_name='baseactor',
            name='follows',
            field=models.ManyToManyField(related_name='_baseactor_follows_+', to='clubeleven_models.BaseActor'),
        ),
    ]
