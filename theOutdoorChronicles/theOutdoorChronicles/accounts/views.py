from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from theOutdoorChronicles.accounts.forms import AppUserCreationForm, ProfileEditForm, ProfileDeleteForm
from theOutdoorChronicles.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')


#     TODO create 'home page' url. Change success_url = reverse_lazy('home page') overriding form.save()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class ProfileDeleteView(DeleteView):
    pass
