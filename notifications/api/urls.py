from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/update$', views.NotificationAPIView.as_view(), name='update'),
    path('', views.NotificationAPIListView.as_view(), name='list'),
]

app_name = 'notifications-api'
