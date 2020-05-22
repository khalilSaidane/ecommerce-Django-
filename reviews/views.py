import statistics

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from comments.forms import CommentForm
from comments.models import CommentReview
from products.models import Product
from reviews.models import Review
from .forms import ReviewCreateForm

@login_required(login_url='/accounts/login')
def create_review_view(request, product_id, *args, **kwargs):
    form = ReviewCreateForm(request.POST or None)
    product = Product.objects.get(id=product_id)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        return redirect('reviews:list-by-product', product.id)
    return render(request, 'reviews/create.html', context={'form': form})

@login_required(login_url='/accounts/login')
def delete_review_view(request, review_id, *args, **kwargs):
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('products:list')


def list_reviews_by_product(request, product_id, *args, **kwargs):
    qs = Review.objects.filter(product_id=product_id)
    product = Product.objects.get(id=product_id)
    product_review_count = product.review_set.count()
    rates = [review.rate for review in qs]
    rate = 0
    if rates:
        rate = statistics.mean(rates)
        rate = float("{:.2f}".format(rate))
    context = {
        'reviews': qs,
        'rate': rate,
        'product_review_count': product_review_count,
        'product': product
    }
    return render(request, 'reviews/list-by-product.html', context)

@login_required(login_url='/accounts/login')
def up_vote_review_view(request, review_id, *args, **kwargs):
    review = Review.objects.toggle_up_vote(user=request.user, review_id=review_id)
    if "products" in request.META['HTTP_REFERER']:
        return redirect('products:detail', review.product_id)
    elif 'reviews/detail' in request.META['HTTP_REFERER']:
        return redirect('reviews:detail', review.id)
    return redirect('reviews:list-by-product', review.product_id)

@login_required(login_url='/accounts/login')
def down_vote_review_view(request, review_id, *args, **kwargs):
    review = Review.objects.toggle_down_vote(user=request.user, review_id=review_id)
    print(review)
    if "products" in request.META['HTTP_REFERER']:
        return redirect('products:detail', review.product_id)
    elif 'reviews/detail' in request.META['HTTP_REFERER']:
        return redirect('reviews:detail', review.id)
    return redirect('reviews:list-by-product', review.product_id)


def detail_review_view(request, review_id, *args, **kwargs):
    review = Review.objects.get(id=review_id)
    form = CommentForm(request.POST or None)
    review = Review.objects.get(id=review_id)
    if form.is_valid() and request.method == 'POST':
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
        form = CommentForm()
    return render(request, 'reviews/detail.html', {'review': review, 'form': form})
