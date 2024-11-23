from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.photos.forms import PhotoCreateForm, PhotoEditForm, PhotoDeleteForm
from theOutdoorChronicles.photos.models import Photo
from theOutdoorChronicles.trail_logs.models import TrailLog

UserModel = get_user_model()


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoCreateForm
    pk_url_kwarg = 'photo_id'
    template_name = 'photos/photo-create-page.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Set relations based on URL parameters
        trail_log_id = self.kwargs.get('trail_log_id')
        trail_id = self.kwargs.get('trail_id')
        animal_id = self.kwargs.get('animal_id')

        if trail_log_id:
            trail_log = get_object_or_404(TrailLog, pk=trail_log_id)
            trail_id = trail_log.trail.pk

        #     TODO possibly move the view to common app and rename to UploadPhoto

        if trail_id:
            form.fields['trail'].widget = forms.HiddenInput()
            form.fields['trail'].initial = trail_id

        if animal_id:
            form.fields['animal'].widget = forms.HiddenInput()
            form.fields['animal'].initial = animal_id

        return form

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()

        trail_log_id = self.kwargs.get('trail_log_id')

        if trail_log_id:
            trail_log = get_object_or_404(TrailLog, pk=trail_log_id)
            trail_log.photos.add(photo)

        return super().form_valid(form)

    def get_success_url(self):
        # Based on context
        if 'trail_id' in self.kwargs:
            return reverse_lazy('trail-details', kwargs={'trail_id': self.kwargs['trail_id']})

        elif 'animal_id' in self.kwargs:
            reverse_lazy('animal-details', kwargs={'animal_id': self.kwargs['animal_id']})

        elif 'trail_log_id' in self.kwargs:
            reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.kwargs['trail_log_id']})

        return reverse_lazy('photo-details', kwargs={'photo_id': self.object.pk})


#     TODO do I really need LoginRequiredMixin
#     TODO make sure uploads happen only from own trail logs (get_queryset())
#     TODO rename to PhotoUploadView


class PhotoDetailView(DetailView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    template_name = 'photos/photo-details-page.html'


#     TODO add extra context with photo details - trails, animals, logs


class PhotoListView(ListView):
    model = Photo
    context_object_name = 'photos'
    template_name = 'photos/photo-list-page.html'


class PhotoEditView(UpdateView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('photo-details', kwargs={'photo_id': self.object.pk})


class PhotoDeleteView(DeleteView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    form_class = PhotoDeleteForm
    template_name = 'photos/photo-delete-page.html'
    success_url = reverse_lazy('photo-list')

    def get_initial(self):
        return self.object.__dict__
