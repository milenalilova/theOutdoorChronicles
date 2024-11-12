from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from theOutdoorChronicles.accounts.forms import AppUserCreationForm

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

#     TODO create 'home page' url. Change success_url = reverse_lazy('home page') overriding form.save()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'


class AppUserLogoutView(LogoutView):
    pass
