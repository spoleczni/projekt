# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_auto_20150511_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text=b'Lista oddzielonych przecinkami tag\xc3\xb3w.', verbose_name=b'Tagi'),
            preserve_default=True,
        ),
    ]
