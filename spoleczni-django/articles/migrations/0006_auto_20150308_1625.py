# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20150308_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subcategory_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
