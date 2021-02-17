import uuid
from datetime import datetime
from django.db import models
from django.db.models import UniqueConstraint
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from blog.models import Post


class Comment(MPTTModel):

    public_id = models.UUIDField(default=uuid.uuid4, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
        )

    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

    visible = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.content[:100]

    def like(self, id):
        user = get_object_or_404(User, id=id)
        if user in self.likes.all():
            self.likes.remove(user)
            return 'unliked'
        else:
            if user in self.dislikes.all():
                self.dislikes.remove(user)
                self.likes.add(user)
                return 'liked and undisliked'
            self.likes.add(user)
            return 'liked'

    def dislike(self, id):
        user = get_object_or_404(User, id=id)
        if user in self.dislikes.all():
            self.dislikes.remove(user)
            return 'undisliked'
        else:
            if user in self.likes.all():
                self.likes.remove(user)
                self.dislikes.add(user)
                return 'disliked and unliked'
            self.dislikes.add(user)
            return 'disliked'


class CommentFlags(models.Model):
    COMMENT_FLAG_REASONS = [('AB', 'Abuse'), ('LA', 'Language'), ('OF', 'Offensive'),
                            ('OT', 'Other'), ('SP', 'Spam'),]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_flags')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_flags')
    reason = models.CharField(max_length=2, choices=COMMENT_FLAG_REASONS, default='OT')

    def __str__(self):
        return str(self.user) + ' | ' + str(self.comment) + ' | ' + str(self.reason)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"], name="limit_flags_by_user"
            )
        ]
        verbose_name_plural = 'Comment Flags'
