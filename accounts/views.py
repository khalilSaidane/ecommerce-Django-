from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView  # LogoutView and PasswordChangeForm are used in urls.py, do not delete it !
from django.views import generic
from django.contrib.auth.models import User


class Register(generic.CreateView):
    model = User
    template_name = 'accounts/register.htm'
    success_url = 'login'
    form_class = UserCreationForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True



class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change-password.html'



