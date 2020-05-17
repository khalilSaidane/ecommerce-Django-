from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:product_id>', views.create_review_view, name='create'),
    path('delete/<int:review_id>', views.delete_review_view, name='delete'),
    path('product/<int:product_id>', views.list_reviews_by_product, name='list-by-product'),
    path('up-vote/<int:review_id>', views.up_vote_review_view, name='up-vote'),
    path('down-vote/<int:review_id>', views.down_vote_review_view, name='down-vote'),
    path('detail/<int:review_id>', views.detail_review_view, name='detail'),
]
app_name = 'reviews'
