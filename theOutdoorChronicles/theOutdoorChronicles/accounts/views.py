from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from theOutdoorChronicles.accounts.forms import AppUserCreationForm, ProfileEditForm, ProfileDeleteForm
from theOutdoorChronicles.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    form_class = ProfileDeleteForm
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home-page')

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        profile = super().get_object(queryset=queryset)
        if profile.user != self.request.user:
            raise PermissionDenied("You cannot delete another user's profile.")
        return self.request.user

    def get_initial(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile.__dict__

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
