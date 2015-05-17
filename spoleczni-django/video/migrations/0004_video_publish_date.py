# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_video_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 16, 16, 50, 31, 875000, tzinfo=utc), verbose_name=b'Data publikacji'),
            preserve_default=True,
        ),
    ]
