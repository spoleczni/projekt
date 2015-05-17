from django.conf.urls import patterns, url
from video.views import VideoDetailView, VideoListView

urlpatterns = patterns('',
                       url(r'^list/(?P<pk>\d+)/$', VideoDetailView.as_view(), name='detail'),
                       url(r'^list/$', VideoListView.as_view(), name='list'),
)

