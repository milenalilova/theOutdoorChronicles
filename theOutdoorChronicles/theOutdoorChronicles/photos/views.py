from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.photos.forms import PhotoCreateForm, PhotoEditForm, PhotoDeleteForm
from theOutdoorChronicles.photos.models import Photo

UserModel = get_user_model()


class PhotoCreateView(CreateView):
    model = Photo
    form_class = PhotoCreateForm
    pk_url_kwarg = 'photo_id'
    template_name = 'photos/photo-create-page.html'

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('photo-details', kwargs={'photo_id': self.object.pk})


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
