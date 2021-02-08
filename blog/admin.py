from django.contrib import admin
from django.shortcuts import reverse
from . models import Post
from django.utils.html import format_html, mark_safe


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
    list_filter = ()