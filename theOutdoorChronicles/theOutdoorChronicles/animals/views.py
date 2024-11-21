from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.forms import AnimalCreateForm, AnimalEditForm, AnimalDeleteForm, AnimalSearchForm
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
    paginate_by = 3
    template_name = 'animals/animal-list-page.html'

    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            return redirect('animal-list')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['animals'] = Animal.objects.all()
        context['animals_found'] = self.get_queryset()
        context['animal_search_form'] = AnimalSearchForm(self.request.GET or None)
        return context

    #
    def get_queryset(self):
        queryset = super().get_queryset()

        animal_name = self.request.GET.get('animal_name' or None)
        if animal_name:
            queryset = queryset.filter(
                Q(common_name__icontains=animal_name) |
                Q(species__icontains=animal_name)
            )
        return queryset


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

# TODO make one search form for animals and trails to get a qyery parm
