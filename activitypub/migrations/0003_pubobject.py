# Generated by Django 2.0.1 on 2018-01-25 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activitypub', '0002_link_preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='PubObject',
            fields=[
                ('common_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activitypub.Common')),
                ('pub_id', models.URLField()),
                ('content', models.TextField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('icon', models.ImageField(null=True, upload_to='')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('published', models.DateTimeField(auto_now_add=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(null=True)),
                ('duration', models.DurationField(null=True)),
                ('attachment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attached_to', to='activitypub.Common')),
                ('attributed_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attributed_from', to='activitypub.Common')),
                ('audience', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audience_for', to='activitypub.Common')),
                ('bcc', models.ManyToManyField(related_name='bcc_reverse', to='activitypub.Common')),
                ('bto', models.ManyToManyField(related_name='bto_reverse', to='activitypub.Common')),
                ('cc', models.ManyToManyField(related_name='cc_reverse', to='activitypub.Common')),
                ('generator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generated', to='activitypub.Common')),
                ('in_reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alt_replies', related_query_name='alt_reply', to='activitypub.Common')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_uses', related_query_name='location_use', to='activitypub.Common')),
                ('preview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preview_for', to='activitypub.Common')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagged', to='activitypub.Common')),
                ('to', models.ManyToManyField(related_name='to_reverse', to='activitypub.Common')),
                ('url', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='activitypub.Link')),
            ],
            bases=('activitypub.common',),
        ),
    ]
