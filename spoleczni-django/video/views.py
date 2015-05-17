from django.shortcuts import render
from video.models import Video
from django.views.generic import TemplateView, DetailView


# Create your views here.
class VideoListView(TemplateView):
    template_name = 'video/list.html'

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        videos = Video.objects.filter(public=True)
        context['videos'] = videos
        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = 'video/index.html'
    context_object_name = 'video'