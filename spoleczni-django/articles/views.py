from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from articles.models import Article, Category
from articles.forms import ArticleFilterForm, ArticleSearchForm
from django.views import generic
from articles.disqus import get_disqus_sso
from taggit.models import Tag


def _get_disqus_sso(user):
    if user.is_authenticated():
        disqus_sso = get_disqus_sso(user)
    else:
        disqus_sso = get_disqus_sso()
    return disqus_sso


class ArticleListView(generic.TemplateView):
    template_name = 'articles/list.html'

    def dispatch(self, request, tag=None, *args, **kwargs):
        self.articles = Article.objects.filter(public=True)
        print request.GET
        self.filter_form = ArticleFilterForm(request.GET)
        self.search_form = ArticleSearchForm(request.GET)
        tags = Tag.objects.all()

        # Tagi
        for tag in tags:
            if tag.name in request.GET:
                self.articles = self.articles.filter(tags__name=tag.name)

        # Filtrowanie po kategorii
        category_filter = request.GET.get('category')
        if category_filter:
            self.articles = self.articles.filter(category=category_filter)

        # Filtrowanie po dacie
        date_filter = request.GET.get('date')
        if date_filter:
            self.articles = self.articles.filter(pub_date=date_filter)

        # Szukanie
        query_filter = request.GET.get('query')
        if query_filter:
            self.articles = self.articles.filter(title__icontains=query_filter)

        return super(ArticleListView, self).dispatch(request, tag, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['articles'] = self.articles
        context['categories'] = Category.objects.all()
        context['filter_form'] = self.filter_form
        context['search_form'] = self.search_form
        return context


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'articles/index.html'

    def dispatch(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        tags = article.tags.all()
        for tag in tags:
            if tag.name in request.GET:
                response = redirect('articles:list')
                response['Location'] += '?%s=' % tag.name
                return response
        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['disqus_sso'] = _get_disqus_sso(self.request.user)
        return context