from django.db import models
from django.urls import reverse


class Post(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'id': self.id})
