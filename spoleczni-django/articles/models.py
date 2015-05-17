# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=500)
    # subcategory_id = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Article(models.Model):
    title = models.CharField(max_length=700, verbose_name="Tytuł")
    body = RichTextField(verbose_name="Treść")
    author = models.ForeignKey(User, null=True, blank=True, verbose_name="Autor")
    category = models.ForeignKey(Category, verbose_name="Kategoria")
    public = models.BooleanField(default=False, verbose_name="Publiczny?")

    tags = TaggableManager(verbose_name="Tagi", help_text="Lista oddzielonych przecinkami tagów.",)

    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name="Data publikacji")

    def __unicode__(self):  # __unicode__ on Python 2
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Ostatnio opublikowany?'

    class Meta:
        verbose_name = "Artykuł"
        verbose_name_plural = "Artykuły"


