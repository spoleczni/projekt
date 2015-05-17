# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, verbose_name=b'Nazwa')),
                ('video', embed_video.fields.EmbedVideoField()),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text=b'Lista oddzielonych przecinkami tag\xc3\xb3w.', verbose_name=b'Tagi')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
