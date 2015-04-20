# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subcategory_id',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
    ]
