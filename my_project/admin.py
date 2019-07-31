from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_date')
    list_filter = ('created_date', 'published_date', 'author')
    search_fields = ('title', 'author')
    date_hierarchy = 'published_date'
    ordering = ['published_date', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
