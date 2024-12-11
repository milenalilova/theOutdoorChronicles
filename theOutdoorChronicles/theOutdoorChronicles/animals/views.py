from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.forms import AnimalCreateForm, AnimalEditForm, AnimalDeleteForm, AnimalSearchForm
from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.common.utils import paginate_and_add_to_context


class AnimalCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalCreateForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-create-page.html'
    permission_required = 'animals.add_animal'

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'animal_id': self.object.pk})


class AnimalDetailsView(LoginRequiredMixin, DetailView):
    model = Animal
    pk_url_kwarg = 'animal_id'
    paginate_by = 3
    template_name = 'animals/animal-details-page.html'

    def get_queryset(self):
        return Animal.objects.prefetch_related('trails', 'photos', 'trail_logs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        public_stats = self.object.trail_logs.aggregate(
            total_observers=Count('user', distinct=True),
            total_logs=Count('id')
        )

        context['public_stats'] = public_stats
        context['animal'] = self.object

        trails = self.object.trails.all()
        context = paginate_and_add_to_context(trails, context, 'trail', self.paginate_by, self.request)
        context['trails_count'] = trails.count()

        trail_logs = self.object.trail_logs.all()
        context = paginate_and_add_to_context(trail_logs, context, 'trail_log', self.paginate_by, self.request)

        photos = self.object.photos.all()
        context = paginate_and_add_to_context(photos, context, 'photo', self.paginate_by, self.request)
        context['photos_count'] = photos.count()

        return context

    def get_template_names(self):
        if 'trails' in self.request.path:
            return 'animals/animal-details-trails-page.html'
        elif 'photos' in self.request.path:
            return 'animals/animal-details-photos-page.html'
        elif 'trail-logs' in self.request.path:
            return 'animals/animal-details-trail-logs-page.html'
        else:
            return self.template_name


class AnimalListView(LoginRequiredMixin, ListView):
    model = Animal
    paginate_by = 3
    template_name = 'animals/animal-list-page.html'

    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            return redirect('animal-list')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal_search_form'] = AnimalSearchForm(self.request.GET or None)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search_query' or None)
        if search_query:
            queryset = queryset.filter(
                Q(common_name__icontains=search_query) |
                Q(species__icontains=search_query)
            )

        return queryset


class AnimalEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalEditForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-edit-page.html'
    permission_required = 'animals.change_animal'

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'animal_id': self.object.pk})


class AnimalDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Animal
    form_class = AnimalDeleteForm
    pk_url_kwarg = 'animal_id'
    template_name = 'animals/animal-delete-page.html'
    success_url = reverse_lazy('animal-list')
    permission_required = 'animals.delete_animal'

    # Gets trails the animal is found on, so they can be displayed before deletion
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trails'] = self.object.trails.all()

        return context

    def get_initial(self):
        return self.object.__dict__
