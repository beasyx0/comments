from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.db import transaction
from comments.models import CommentFlags

@receiver(signals.post_save, sender=CommentFlags)
def comment_check_flag_limit(sender, instance, created, **kwargs):
	'''Checks if the flag.comment is at or over the limit of flags allowed
	and if so automatically switches the comments visibility to False'''
	if instance.comment.comment_flags.count() >= settings.COMMENTS_FLAG_LIMIT:
		comment = instance.comment
		comment.visible = False
		comment.save()
