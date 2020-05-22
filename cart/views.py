from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models import Product
from .models import CartProduct

@login_required(login_url='/accounts/login')
def my_cart_view(request, *args, **kwargs):
    qs = CartProduct.objects.filter(user=request.user)
    total_price = sum([x.product.price for x in qs])
    return render(request, 'cart/my-cart.html', {'items': qs, 'total_price': total_price})

@login_required(login_url='/accounts/login')
def add_product_to_cart(request, product_id, *args, **kwargs):
    product = Product.objects.get(id=product_id)
    qs = CartProduct.objects.filter(user=request.user)
    if product not in [c.product for c in qs]:
        cart_product = CartProduct(user=request.user, product=product)
        cart_product.save()
    return redirect('cart:my_cart')


def remove_product_from_cart(request, product_id, *args, **kwargs):
    cart_product = CartProduct.objects.filter(user=request.user, product_id=product_id)
    if cart_product.exists():
        cart_product.delete()
    return redirect('cart:my_cart')
