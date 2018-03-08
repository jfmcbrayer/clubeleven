# Generated by Django 2.0.1 on 2018-03-08 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubeleven_models', '0004_baseactor_json'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('baseactor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.BaseActor')),
            ],
            bases=('clubeleven_models.baseactor',),
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_type', models.CharField(choices=[('A', 'Accept'), ('R', 'Reject'), ('T', 'Tentative')], max_length=20)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='clubeleven_models.Event')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='clubeleven_models.BaseActor')),
                ('response', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response', to='clubeleven_models.BasePost')),
            ],
        ),
        migrations.CreateModel(
            name='MediaPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.Post')),
                ('media', models.FileField(upload_to='')),
            ],
            bases=('clubeleven_models.post',),
        ),
        migrations.RemoveField(
            model_name='persona',
            name='user',
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='clubeleven_models.Persona'),
        ),
    ]
