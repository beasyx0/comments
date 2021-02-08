from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from comments.models import Post, Comment
from comments.forms import CommentForm


@login_required
# New parameter parent_comment_id
def post_comment(request, post_id, parent_comment_id=None):
    post = get_object_or_404(Post, id=post_id)

    # Processing POST requests
    if request.method == 'POST':
        reply_form = CommentForm(request.POST)
        if reply_form.is_valid():
            new_comment = reply_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user

            # Secondary response
            if parent_comment_id:
                parent_comment = get_object_or_404(
                    Comment, public_id=parent_comment_id)
                new_comment.parent = parent_comment
                new_comment.save()
                return redirect(
                    str(post.get_absolute_url()) 
                    + '#comment_' 
                    + str(parent_comment.public_id)
                    )

            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("The form is incorrect, please fill it in again.")
    else:
        return HttpResponse("Only GET/POST requests are accepted.")


def comment_edit(request, comment_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, public_id=comment_id)
    comment_edit_form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST':
        if comment_edit_form.is_valid():
            comment_edit_form.save()
            return redirect(
                    str(post.get_absolute_url()) 
                    + '#comment_' 
                    + str(comment.parent.public_id)
                    )
    context = {
        'comment': comment,
        'comment_edit_form': comment_edit_form,
    }
    return render(request, 'comments/edit.html', context)


def comment_delete_confirm(request, comment_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, public_id=comment_id)
    next = request.GET.get('next') + '#comments'
    if request.method == 'POST':
        comment.delete()
        if comment.parent:
            return redirect(
                str(post.get_absolute_url()) 
                + '#comment_' 
                + str(comment.parent.public_id)
                )
        else:
            return redirect(next)
    context = {
        'comment': comment,
    }
    return render(request, 'comments/delete.html', context)


def like_comment(request):
    liked = None
    comment_id = None
    likes_count = None
    dislikes_count = None
    status = 400
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        if user.is_authenticated:
            comment_id = request.POST.get('comment_id', None)
            comment = get_object_or_404(Comment, public_id=comment_id)
            liked = comment.like(user.id)
            likes_count = comment.likes.count()
            dislikes_count = comment.dislikes.count()
            status = 200
    return JsonResponse({"liked": liked, 
                        "comment_id": comment_id,
                        "likes_count": likes_count,
                        "dislikes_count": dislikes_count,}, 
                        status=status)


def dislike_comment(request):
    disliked = None
    comment_id = None
    likes_count = None
    dislikes_count = None
    status = 400
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        if user.is_authenticated:
            comment_id = request.POST.get('comment_id', None)
            comment = get_object_or_404(Comment, public_id=comment_id)
            disliked = comment.dislike(user.id)
            likes_count = comment.likes.count()
            dislikes_count = comment.dislikes.count()
            status = 200
    return JsonResponse({"disliked": disliked, 
                        "comment_id": comment_id,
                        "likes_count": likes_count,
                        "dislikes_count": dislikes_count,}, 
                        status=status)
