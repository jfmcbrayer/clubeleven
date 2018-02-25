# Generated by Django 2.0.1 on 2018-02-25 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=80)),
                ('profile_url', models.URLField(max_length=2048)),
                ('inbox_url', models.URLField(max_length=2048)),
                ('outbox_url', models.URLField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='BasePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, null=True)),
                ('media_type', models.CharField(max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('baseactor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.BaseActor')),
                ('default_visibility', models.CharField(choices=[('PUB', 'Public'), ('FL', 'Followers only'), ('MUT', 'Friends only'), ('LIST', 'Listed people only')], max_length=8)),
                ('is_searchable', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clubeleven_models.User')),
            ],
            bases=('clubeleven_models.baseactor',),
        ),
        migrations.AddField(
            model_name='baseactor',
            name='local_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clubeleven_models.BaseActor'),
        ),
    ]
