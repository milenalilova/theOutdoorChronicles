from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.forms import AnimalCreateForm, AnimalEditForm, AnimalDeleteForm
from theOutdoorChronicles.animals.models import Animal


class AnimalCreateView(PermissionRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalCreateForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-create-page.html'
    permission_required = 'animals.add_animal'

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'animal_id': self.object.pk})


class AnimalDetailsView(DetailView):
    model = Animal
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.object
        context['trails'] = self.object.trails.all()
        return context


class AnimalListView(ListView):
    model = Animal
    context_object_name = 'animals'
    template_name = 'animals/animal-list-page.html'


class AnimalEditView(PermissionRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalEditForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-edit-page.html'
    permission_required = 'animals.change_animal'

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'animal_id': self.object.pk})


class AnimalDeleteView(PermissionRequiredMixin, DeleteView):
    model = Animal
    form_class = AnimalDeleteForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-delete-page.html'
    success_url = reverse_lazy('animal-list')
    permission_required = 'animals.delete_animal'

    # gets trails the animal os found on, so they can be displayed before deletion
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trails'] = self.object.trails.all()
        return context

    def get_initial(self):
        return self.object.__dict__
