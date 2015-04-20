from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from articles import models as m

def index(request):
    recent_articles = m.Article.objects.filter(public=True).order_by('-pub_date').values()
    return render_to_response('home/index.html',
                              {'recent_articles': recent_articles},
                              context_instance=RequestContext(request))

