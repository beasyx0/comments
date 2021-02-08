from django.contrib import admin
from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'post', 'content', 'parent',)
    list_filter = ('created', 'user', 'post', 'content', 'parent',)
