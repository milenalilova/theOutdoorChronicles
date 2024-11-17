from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.forms import AnimalCreateForm, AnimalEditForm, AnimalDeleteForm
from theOutdoorChronicles.animals.models import Animal


class AnimalCreateView(CreateView):
    model = Animal
    form_class = AnimalCreateForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-create-page.html'

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'animal_id': self.object.pk})


class AnimalDetailsView(DetailView):
    model = Animal
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-details-page.html'


#      TODO add a list of trails the animal is found on in the context


class AnimalListView(ListView):
    model = Animal
    context_object_name = 'animals'
    template_name = 'animals/animal-list-page.html'


class AnimalEditView(UpdateView):
    model = Animal
    form_class = AnimalEditForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'animal_id': self.object.pk})


class AnimalDeleteView(DeleteView):
    model = Animal
    form_class = AnimalDeleteForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-delete-page.html'
    success_url = reverse_lazy('animal-list')

    def get_initial(self):
        return self.object.__dict__
