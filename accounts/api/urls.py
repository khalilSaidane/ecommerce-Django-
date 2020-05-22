from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
]
app_name ='accounts-api'
