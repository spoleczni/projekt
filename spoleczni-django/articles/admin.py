from django.contrib import admin
from articles.models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Article', {'fields': ['pub_date', 'body']}),
    ]

    list_display = ('title', 'author', 'pub_date', 'was_published_recently')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

admin.site.register(Article, ArticleAdmin)