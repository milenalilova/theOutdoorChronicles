import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
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

        if trail_id:
            form.fields['trail'].widget = forms.HiddenInput()
            form.fields['trail'].initial = trail_id

        if animal_id:
            form.fields['animal'].widget = forms.HiddenInput()
            form.fields['animal'].initial = animal_id
        #     TODO Display just animals existing on trail or raise error

        return form

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()

        trail_log_id = self.kwargs.get('trail_log_id')

        if trail_log_id:
            trail_log = get_object_or_404(TrailLog, pk=trail_log_id)
            if trail_log.user == self.request.user:  # only owners of the trail_log can upload photos
                trail_log.photos.add(photo)
            else:
                raise PermissionDenied("You do not own this TrailLog.")

        return super().form_valid(form)

    def get_success_url(self):
        # Based on context
        if 'trail_id' in self.kwargs:
            return reverse_lazy('trail-details',
                                kwargs={'trail_id': self.kwargs['trail_id']}) + '#photo-upload-section'

        elif 'animal_id' in self.kwargs:
            return reverse_lazy('animal-details',
                                kwargs={'animal_id': self.kwargs['animal_id']}) + '#photo-upload-section'

        elif 'trail_log_id' in self.kwargs:
            return reverse_lazy('trail-log-details',
                                kwargs={'trail_log_id': self.kwargs['trail_log_id']}) + '#photo-upload-section'

        return reverse_lazy('photo-details',
                            kwargs={'photo_id': self.object.pk}) + '#photo-upload-section'


class PhotoDetailView(DetailView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    template_name = 'photos/photo-details-page.html'

    def get_queryset(self):
        return Photo.objects.select_related('user', 'trail', 'animal').prefetch_related('trail_logs')


class PhotoListView(ListView):
    model = Photo
    context_object_name = 'photos'
    paginate_by = 9
    template_name = 'photos/photo-list-page.html'


#     TODO this view maybe unnecessary


class PhotoEditView(UpdateView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('photo-details', kwargs={'photo_id': self.object.pk})


class PhotoDeleteView(DeleteView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    form_class = PhotoDeleteForm
    template_name = 'photos/photo-delete-page.html'
    success_url = reverse_lazy('photo-list')

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trail'] = self.object.trail
        context['animal'] = self.object.animal
        context['trail_logs'] = self.object.trail_logs.all()
        return context

    def get_initial(self):
        return self.object.__dict__

    def post(self, request, *args, **kwargs):
        # Get the photo before deletion
        photo = self.get_object()

        # Store the image path before deletion
        image_path = None
        if photo.image:
            # Construct the full path to the image
            image_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))

        # Use the parent class's delete method
        response = super().post(request, *args, **kwargs)

        # Delete the image file from the filesystem
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        return response

    # Option 2 also works
    # def post(self, request, *args, **kwargs):
    #     # Use get_object() to fetch the object
    #     photo = self.get_object()
    #
    #     # Delete the image file from the filesystem
    #     if photo.image:
    #         # Construct the full path to the image
    #         image_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))
    #
    #         # Check if the file exists and delete it
    #         if os.path.exists(image_path):
    #             os.remove(image_path)
    #
    #     # Delete the database record
    #     photo.delete()
    #
    #     # Redirect to success URL
    #     return HttpResponseRedirect(reverse_lazy('photo-list'))
1