from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from articles.models import Article, Category
from articles.forms import ArticleFilterForm, ArticleSearchForm
from django.views import generic
from articles.disqus import get_disqus_sso


def _get_disqus_sso(user):
    if user.is_authenticated():
        disqus_sso = get_disqus_sso(user)
    else:
        disqus_sso = get_disqus_sso()
    return disqus_sso


class ArticleListView(generic.TemplateView):
    template_name = 'articles/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.articles = Article.objects.filter(public=True)
        print request.GET
        self.filter_form = ArticleFilterForm(request.GET)
        self.search_form = ArticleSearchForm(request.GET)

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

        return super(ArticleListView, self).dispatch(request, *args, **kwargs)

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

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['disqus_sso'] = _get_disqus_sso(self.request.user)
        return context