# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_auto_20150516_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 16, 17, 28, 53, 437000, tzinfo=utc), verbose_name=b'Data publikacji'),
            preserve_default=True,
        ),
    ]
