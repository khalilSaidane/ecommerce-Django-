from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:review_id>', views.create_comment_view, name='create'),
    path('create/<int:review_id>/<int:comment_id>', views.create_child_comment_view, name='create_child'),
    path('detail/<int:comment_id>', views.detail_comment_view, name='detail'),
]
app_name = 'comments'
