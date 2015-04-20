# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20150316_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory_id',
        ),
    ]
