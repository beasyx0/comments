from django.contrib import admin
from django.urls import path, include

from comments.views import post_comment, comment_edit, comment_delete_confirm, like_comment, dislike_comment, flag_comment


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    # Existing code to handle first-level replies
    path('post-comment/<int:post_id>/', post_comment, name='post-comment'),
    # Added code to handle secondary replies
    path('post-comment/<int:post_id>/<uuid:parent_comment_id>/', post_comment, name='comment-reply'),
    path('comment-edit/<uuid:comment_id>/<int:post_id>/', comment_edit, name='comment-edit'),
    path('comment-delete-confirm/<uuid:comment_id>/<int:post_id>/', comment_delete_confirm, name='comment-delete-confirm'),
    path('like-comment/', like_comment, name='like-comment'),
    path('dislike-comment/', dislike_comment, name='dislike-comment'),
    path('flag-comment/<uuid:comment_id>/', flag_comment, name='flag-comment'),
]