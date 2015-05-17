# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_auto_20150516_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='publish_date',
            field=models.DateTimeField(verbose_name=b'Data publikacji'),
            preserve_default=True,
        ),
    ]
