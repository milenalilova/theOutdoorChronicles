from datetime import timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.trails.forms import TrailCreateForm, TrailEditForm, TrailDeleteForm, TrailSearchForm
from theOutdoorChronicles.trails.models import Trail


class TrailCreateView(PermissionRequiredMixin, CreateView):
    model = Trail
    form_class = TrailCreateForm
    pk_url_kwarg = 'trail_id'
    template_name = 'trails/trail-create-page.html'
    permission_required = 'trails.add_trail'

    def get_success_url(self):
        return reverse_lazy('trail-details', kwargs={'trail_id': self.object.pk})


class TrailDetailsView(DetailView):
    model = Trail
    pk_url_kwarg = 'trail_id'
    paginate_by = 3
    template_name = 'trails/trail-details-page.html'

    def get_queryset(self):
        return Trail.objects.prefetch_related('animals', 'photos', 'trail_logs')

    def paginate_context(self, queryset, page_param, per_page):
        page_number = self.request.GET.get(page_param, 1)
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get public statistics
        public_stats = self.object.trail_logs.aggregate(
            total_hikers=Count('user', distinct=True),
            total_logs=Count('id'),
            avg_duration=Avg('duration') or timedelta(0),
        )

        context['public_stats'] = public_stats
        context['trail'] = self.object

        trail_logs = self.object.trail_logs.all()
        context['trail_logs_paginated'] = self.paginate_context(trail_logs, 'page_logs', self.paginate_by)
        context['trail_logs_page_param'] = 'page_logs'

        animals = self.object.animals.all()
        context['animals_count'] = animals.count()
        context['animals_paginated'] = self.paginate_context(animals, 'page_animals', self.paginate_by)
        context['animals_page_param'] = 'page_animals'

        photos = self.object.photos.all()
        context['photos_count'] = photos.count()
        context['photos_paginated'] = self.paginate_context(photos, 'page_photos', self.paginate_by)
        context['photos_page_param'] = 'page_photos'

        return context

    def get_template_names(self):
        if 'animals' in self.request.path:
            return 'trails/trail-details-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trails/trail-details-photos-page.html'
        elif 'trail-logs' in self.request.path:
            return 'trails/trail-details-trail-logs-page.html'
        else:
            return self.template_name


class TrailListView(ListView):
    model = Trail
    paginate_by = 3
    template_name = 'trails/trail-list-page.html'

    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            return redirect('trail-list')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trails_search_form'] = TrailSearchForm(self.request.GET or None)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search_query' or None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        return queryset


class TrailEditView(PermissionRequiredMixin, UpdateView):
    model = Trail
    form_class = TrailEditForm
    pk_url_kwarg = 'trail_id'
    template_name = 'trails/trail-edit-page.html'
    permission_required = 'trails.change_trail'

    def get_success_url(self):
        return reverse_lazy('trail-details', kwargs={'trail_id': self.object.pk})


class TrailDeleteView(PermissionRequiredMixin, DeleteView):
    model = Trail
    form_class = TrailDeleteForm
    pk_url_kwarg = 'trail_id'
    template_name = 'trails/trail-delete-page.html'
    success_url = reverse_lazy('trail-list')
    permission_required = 'trails.delete_trail'

    # displays all related data before deletion
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = self.object.animals.all()
        context['photos'] = self.object.photos.count()
        context['trail_logs'] = self.object.trail_logs.count()
        return context

    def get_initial(self):
        return self.object.__dict__
