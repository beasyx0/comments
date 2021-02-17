from django.shortcuts import render, get_object_or_404
from blog.models import Post
from comments.forms import CommentForm, CommentFlagForm


def index(request):
	return render(request, 'blog/index.html')


def post_detail(request, id):
	post = get_object_or_404(Post, id=id)
	comments = post.comments.filter(visible=True)
	comment_reply_form = CommentForm(request.POST or None)
	comment_flag_form = CommentFlagForm(request.POST or None)
	context = {
		'post': post,
		'comments': comments,
		'comment_reply_form': comment_reply_form,
		'comment_flag_form': comment_flag_form,
	}
	return render(request, 'blog/post-detail.html', context)