# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20150516_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='public',
            field=models.BooleanField(default=False, verbose_name=b'Publiczny?'),
            preserve_default=True,
        ),
    ]
