# Generated by Django 2.0.1 on 2018-03-12 19:47

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('json', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, null=True)),
                ('media_type', models.CharField(max_length=80, null=True)),
                ('icon', models.ImageField(null=True, upload_to='')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_type', models.CharField(choices=[('A', 'Accept'), ('R', 'Reject'), ('T', 'Tentative')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('baseactor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.BaseActor')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            bases=('clubeleven_models.baseactor',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('basepost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.BasePost')),
                ('href', models.URLField(max_length=2048)),
                ('hreflang', models.CharField(max_length=8, null=True)),
                ('height', models.PositiveSmallIntegerField()),
                ('width', models.PositiveSmallIntegerField()),
                ('preview', models.TextField()),
            ],
            bases=('clubeleven_models.basepost',),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('baseactor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.BaseActor')),
                ('default_visibility', models.CharField(choices=[('PUB', 'Public'), ('FL', 'Followers only'), ('MUT', 'Friends only'), ('LIST', 'Listed people only')], max_length=8)),
                ('is_searchable', models.BooleanField(default=True)),
                ('avatar', models.ImageField(null=True, upload_to='')),
            ],
            bases=('clubeleven_models.baseactor',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('basepost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.BasePost')),
                ('content', models.TextField()),
                ('source', models.TextField()),
            ],
            bases=('clubeleven_models.basepost',),
        ),
        migrations.AddField(
            model_name='invite',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='clubeleven_models.BaseActor'),
        ),
        migrations.AddField(
            model_name='invite',
            name='response',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response', to='clubeleven_models.BasePost'),
        ),
        migrations.AddField(
            model_name='basepost',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clubeleven_models.BaseActor'),
        ),
        migrations.AddField(
            model_name='baseactor',
            name='local_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.Post')),
            ],
            bases=('clubeleven_models.post',),
        ),
        migrations.CreateModel(
            name='MediaPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.Post')),
                ('media', models.FileField(upload_to='')),
            ],
            bases=('clubeleven_models.post',),
        ),
        migrations.AddField(
            model_name='invite',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='clubeleven_models.Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='clubeleven_models.Persona'),
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clubeleven_models.Comment')),
                ('type', models.CharField(choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike'), ('SEEN', 'Seen')], max_length=8)),
                ('emojo', models.CharField(max_length=16, null=True)),
                ('shortcode', models.CharField(max_length=16, null=True)),
            ],
            bases=('clubeleven_models.comment',),
        ),
        migrations.AddField(
            model_name='comment',
            name='conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='clubeleven_models.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='clubeleven_models.Post'),
        ),
    ]
