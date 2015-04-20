from django.contrib import admin
from django import forms
import articles.models as articles


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Article', {'fields': ['pub_date', 'category', 'body', 'public']}),
    ]

    list_display = ('title', 'author', 'category', 'pub_date', 'was_published_recently', 'public')
    list_editable = ('public', )
    list_filter = ('public',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(articles.Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Kategoria', {'fields': ['name', ]}),
    ]
    list_display = ('name',)
    # ordering = ('subcategory_id',)

    # def subcategory_name(self, obj):
    #     return articles.Category.objects.get(id=obj.subcategory_id).name


admin.site.register(articles.Category, CategoryAdmin)
