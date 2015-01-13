import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=700)
    body = models.TextField()
    author = models.ForeignKey(User, null=True, blank=True)

    pub_date = models.DateTimeField('date published', default=datetime.datetime.now)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
