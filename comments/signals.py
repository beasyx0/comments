from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.db import transaction, IntegrityError
from comments.models import CommentFlags


@receiver(signals.post_save, sender=CommentFlags)
def comment_check_flag_limit(sender, instance, created, **kwargs):
	'''Checks if the flag.comment is at or over the limit of flags allowed
	and if so automatically switches the comments visibility to False'''
	if instance.comment.comment_flags.count() >= settings.COMMENTS_FLAG_LIMIT:
		comment = instance.comment
		comment.visible = False
		comment.save()


@receiver(signals.pre_save, sender=CommentFlags)
def user_check_flag_limit(sender, instance, **kwargs):
	if instance.id is None:
		if instance.user.comment_flags.all().count() >= settings.COMMENTS_USER_FLAG_LIMIT:
			raise IntegrityError('User has too many flags')