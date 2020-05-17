from django.shortcuts import render

from comments.models import CommentReview
from reviews.models import Review
from .forms import CommentForm


def create_comment_view(request, review_id, *args, **kwargs):
    form = CommentForm(request.POST or None)
    review = Review.objects.get(id=review_id)
    if form.is_valid() and request.method == 'POST':
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
    return render(request, 'comments/create.html', {'form': form})


def create_child_comment_view(request, review_id, comment_id, *args, **kwargs):
    child_form = CommentForm(request.POST or None)
    review = Review.objects.get(id=review_id)
    parent_comment = CommentReview.objects.get(id=comment_id)
    if child_form.is_valid() and request.method == 'POST':
        comment = child_form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.is_child = True
        comment.save()
        parent_comment.childs.add(comment)
        parent_comment.save()
        child_form = CommentForm()
    return render(request, 'comments/create-child.html', {'child_form': child_form})


def detail_comment_view(request, comment_id, *args, **kwargs):
    comment = CommentReview.objects.get(id=comment_id)
    child_form = CommentForm(request.POST or None)
    review = comment.review
    parent_comment = CommentReview.objects.get(id=comment_id)
    if child_form.is_valid() and request.method == 'POST':
        comment = child_form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.is_child = True
        comment.save()
        parent_comment.childs.add(comment)
        parent_comment.save()
        child_form = CommentForm()
    return render(request, 'comments/detail.html', {'comment': comment, 'child_form': child_form})
