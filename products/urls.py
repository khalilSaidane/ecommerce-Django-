from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_product_view, name='create'),
    path('list/', views.list_product_view, name='list'),
    path('<int:id>', views.product_detail_view, name='detail'),
]
app_name = 'products'
