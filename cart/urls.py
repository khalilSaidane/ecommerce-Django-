from django.urls import path
from . import views

urlpatterns = [
    path('my-cart/', views.my_cart_view, name='my_cart'),
    path('remove-from-cart/<int:product_id>', views.remove_product_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>', views.add_product_to_cart, name='add_to_cart'),
]
app_name = 'cart'
