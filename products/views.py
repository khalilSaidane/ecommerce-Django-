import statistics

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateProductForm
from .models import Product


@login_required(login_url='/accounts/login')
def create_product_view(request, *args, **kwargs):
    form = CreateProductForm(request.POST or None, request.FILES or None)
    print(request)
    if form.is_valid() and request.method == 'POST':
        form.save()
    return render(request, 'products/create.html', {'form': form})


def list_product_view(request, *args, **kwargs):
    qs = Product.objects.all()
    return render(request, 'products/list.html', {'products': qs})


def product_detail_view(request, id, *args, **kwargs):
    product = Product.objects.get(id=id)
    reviews = product.review_set.all()
    product_review_count = product.review_set.count()
    rate = 0
    if reviews.count() > 0:
        rate = statistics.mean([review.rate for review in reviews])
        rate = float("{:.2f}".format(rate))
    context = {
        'product': product,
        'reviews': reviews[:2],
        'rate': rate,
        'product_review_count': product_review_count
    }
    return render(request, 'products/detail.html', context)
