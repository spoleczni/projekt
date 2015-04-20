# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20150308_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
