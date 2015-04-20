# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20150316_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(verbose_name=b'Autor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name=b'Tre\xc5\x9b\xc4\x87'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name=b'Kategoria', to='articles.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data publikacji'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='public',
            field=models.BooleanField(default=False, verbose_name=b'Publiczny?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=700, verbose_name=b'Tytu\xc5\x82'),
            preserve_default=True,
        ),
    ]
