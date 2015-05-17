from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from video.models import Video, Category
from django.utils import timezone


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Kategoria', {'fields': ['name', ]}),
    ]
    list_display = ('name',)


class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Video', {'fields': ['category', 'video', 'public', 'tags']}),
    ]

    list_display = ('name', 'video', 'category', 'author')
    list_filter = ('name', )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        if not obj.publish_date:
            obj.publish_date = timezone.now()
        super(VideoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)