# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_category_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='tags',
        ),
    ]
