from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from comments.models import Post, Comment
from comments.forms import CommentForm, CommentFlagForm

from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["POST"])
def post_comment(request, post_id, parent_comment_id=None):
    post = get_object_or_404(Post, id=post_id)
    reply_form = CommentForm(request.POST)
    if reply_form.is_valid():
        new_comment = reply_form.save(commit=False) # add post and user to comment
        new_comment.post = post
        new_comment.user = request.user

        # Secondary response
        if parent_comment_id:
            parent_comment = get_object_or_404(
                Comment, public_id=parent_comment_id)
            new_comment.parent = parent_comment

        new_comment.save()
        messages.success(request, 'New comment success')
        return redirect(
            str(post.get_absolute_url()) 
            + '#comment_' 
            + str(new_comment.public_id)
            )
    else:
        messages.error(request, 'Something went wrong with your form')
        return redirect(
            str(post.get_absolute_url()) 
            + '#comments'
            )


def comment_edit(request, comment_id, post_id):
    '''Edits existing comment object'''
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, public_id=comment_id)
    comment_edit_form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST':
        if comment_edit_form.is_valid():
            comment_edit_form.save()
            if comment.parent: # redirect back to parent comment
                return redirect( 
                    str(post.get_absolute_url()) 
                    + '#comment_' 
                    + str(comment.parent.public_id)
                    )
            else: # or back to the same comment edited
                return redirect(
                    str(post.get_absolute_url()) 
                    + '#comment_' 
                    + str(comment.public_id)
                    )
    context = {
        'comment': comment,
        'comment_edit_form': comment_edit_form,
    }
    return render(request, 'comments/edit.html', context)


def comment_delete_confirm(request, comment_id, post_id):
    '''Confirms deletion of a comment'''
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, public_id=comment_id)
    next = request.GET.get('next') + '#comments' # comment section just in case
    if request.method == 'POST':
        comment.delete()
        if comment.parent: # redirect back to parent comment
            return redirect(
                str(post.get_absolute_url()) 
                + '#comment_' 
                + str(comment.parent.public_id)
                )
        else:
            return redirect(next) # or back to the comments section
    context = {
        'comment': comment,
    }
    return render(request, 'comments/delete.html', context)


def like_comment(request):
    '''Likes a comment. Called from jquery ajax'''
    liked = None
    comment_id = None
    likes_count = None
    dislikes_count = None
    status = 400 # if anything fails return bad response
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        if user.is_authenticated:
            comment_id = request.POST.get('comment_id', None)
            comment = get_object_or_404(Comment, public_id=comment_id)
            liked = comment.like(user.id) # call model method
            likes_count = comment.likes.count() # send back to front end
            dislikes_count = comment.dislikes.count()
            status = 200
    return JsonResponse({"liked": liked, 
                        "comment_id": comment_id,
                        "likes_count": likes_count,
                        "dislikes_count": dislikes_count,}, 
                        status=status)


@login_required
@require_http_methods(["POST"])
def dislike_comment(request):
    '''Dislikes a comment. Called from jquery ajax'''
    disliked = None
    comment_id = None
    likes_count = None
    dislikes_count = None
    status = 400 # if anything fails return bad response
    if request.method == 'POST' and request.is_ajax(): # make sure its ajax
        user = request.user
        if user.is_authenticated:
            comment_id = request.POST.get('comment_id', None)
            comment = get_object_or_404(Comment, public_id=comment_id)
            disliked = comment.dislike(user.id) # call model method
            likes_count = comment.likes.count() # send back to front end
            dislikes_count = comment.dislikes.count()
            status = 200
    return JsonResponse({"disliked": disliked, 
                        "comment_id": comment_id,
                        "likes_count": likes_count,
                        "dislikes_count": dislikes_count,}, 
                        status=status)


@login_required
@require_http_methods(["POST"])
def flag_comment(request, comment_id):
    '''Flags a comment and redirects back based on the comments \
    visibility after being flagged'''
    user = request.user
    comment = get_object_or_404(Comment, public_id=comment_id)
    # how many times has this person flagged this comment
    user_flag_count = user.comment_flags.all().filter(comment=comment).count()
    comment_flag_form = CommentFlagForm(request.POST or None)
    comment_url = str(comment.post.get_absolute_url()) + '#comment_' + str(comment.public_id)
    comments_section_url = str(comment.post.get_absolute_url()) + '#comments'
    if user_flag_count >= 3: # if already flagged 3 times redirect with message
        messages.error(request, 'You already flagged that one enough. Thanks.')
        return redirect(comment_url)
    if comment_flag_form.is_valid():
        new_flag = comment_flag_form.save(commit=False)
        new_flag.user = request.user # add current user
        new_flag.comment = comment # add specified comment
        new_flag.save() # comments.signals.comment_check_flag_limit
        messages.success(request, f'Comment Flagged. Thanks {user.username}!') # message for user
        comment.refresh_from_db() # see if the signal toggled visibility
        if comment.visible: # redirect back to comment if still visible
            return redirect(comment_url)
        else: # or back to the comments section
            return redirect(comments_section_url)
    else: # if form is not valid back to the comment with a message
        messages.error('Something went wrong, please try again')
        return redirect(comment_url)
