# -*- coding: utf-8 -*-
from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=500)
    # subcategory_id = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Video(models.Model):
    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"

    name = models.CharField(verbose_name="Nazwa", max_length=1024)
    video = EmbedVideoField()
    public = models.BooleanField(default=False, verbose_name="Publiczny?")
    publish_date = models.DateTimeField(verbose_name="Data publikacji")
    author = models.ForeignKey(User, null=True, blank=True, verbose_name="Autor")
    category = models.ForeignKey(Category, null=True, verbose_name="Kategoria")
    tags = TaggableManager(verbose_name="Tagi", help_text="Lista oddzielonych przecinkami tagów.",)