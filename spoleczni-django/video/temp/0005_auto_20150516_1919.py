# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0004_video_publish_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategorie',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='video',
            name='author',
            field=models.ForeignKey(verbose_name=b'Autor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(default=datetime.datetime(2015, 5, 16, 17, 19, 25, 951000, tzinfo=utc), verbose_name=b'Kategoria', to='video.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 16, 17, 18, 58, 579000, tzinfo=utc), verbose_name=b'Data publikacji'),
            preserve_default=True,
        ),
    ]
