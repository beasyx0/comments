from django.contrib import admin
from comments.models import Comment, CommentFlags


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'post', 'content', 'visible', 'parent',)
    list_filter = ('created', 'user', 'post', 'content', 'visible', 'parent',)
    actions = ['toggle_visibility']

    def toggle_visibility(self, request, queryset):
        for comment in queryset:
            if comment.visible:
                comment.visible = False
            else:
                comment.visible = True
            comment.save()
        self.message_user(request, 'Visibility toggled')


@admin.register(CommentFlags)
class CommentFlagsAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason',)
    list_filter = ()