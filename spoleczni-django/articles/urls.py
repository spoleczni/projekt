from django.conf.urls import patterns, url
from articles.views import ArticleView, ArticleListView

urlpatterns = patterns('',
                       url(r'^list/(?P<pk>\d+)/$', ArticleView.as_view(), name='detail'),
                       url(r'^list/$', ArticleListView.as_view(), name='list'),
)
