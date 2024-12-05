from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.photos.models import Photo
from theOutdoorChronicles.trail_logs.forms import TrailLogCreateForm, TrailLogEditForm, TrailLogDeleteForm
from theOutdoorChronicles.trail_logs.models import TrailLog
from theOutdoorChronicles.trails.models import Trail


class TrailLogCreateView(LoginRequiredMixin, CreateView):
    model = TrailLog
    form_class = TrailLogCreateForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-create-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trail_id = self.kwargs.get('trail_id')
        if trail_id:
            trail = get_object_or_404(Trail, pk=trail_id)
            context['trail'] = trail
            context['previous_logs_count'] = TrailLog.objects.filter(
                user=self.request.user,
                trail=trail
            ).count()

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        trail_id = self.kwargs.get('trail_id')
        if trail_id:
            trail = get_object_or_404(Trail, pk=trail_id)
            form.fields['trail'].widget = forms.HiddenInput()
            form.fields['trail'].initial = trail_id
            form.fields['animals_spotted'].queryset = trail.animals.all()

        return form

    def form_valid(self, form):
        trail_log = form.save(commit=False)
        trail_log.user = self.request.user
        trail_log.save()

        trail_id = self.kwargs.get('trail_id')
        if trail_id:
            trail = get_object_or_404(Trail, pk=trail_id)
            trail.trail_logs.add(trail_log)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.object.pk})


class TrailLogDetailsView(DetailView):
    model = TrailLog
    context_object_name = 'trail_log'
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = self.object.animals.all()
        context['photos'] = self.object.photos.all()
        return context

    def get_queryset(self):
        return TrailLog.objects.select_related('trail').prefetch_related('animals', 'photos')

        # filter(user=self.request.user)  # only log's users can see details

    def get_template_names(self):
        if 'animals' in self.request.path:
            return 'trail_logs/trail-log-details-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail-log-details-photos-page.html'
        else:
            return self.template_name


class TrailLogListView(ListView):  # all hiking user experience
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 5
    template_name = 'trail_logs/trail-logs-list-page.html'

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail') \
            .prefetch_related('animals', 'photos') \
            .order_by('-date_completed')

    def paginate_context(self, queryset, page_param, per_page):
        page_number = self.request.GET.get(page_param, 1)
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_trails = TrailLog.objects.filter(user=self.request.user) \
            .values('trail') \
            .distinct() \
            .count()

        # uses reverse relation from Trail
        total_length = Trail.objects.filter(trail_logs__user=self.request.user) \
                           .aggregate(total_length=Sum('length'))['total_length'] or 0

        # uses reverse relation from Animal
        total_species_seen = Animal.objects.filter(trail_logs__user=self.request.user) \
            .distinct() \
            .count()

        trail_logs_count = self.get_queryset().count()
        photos_count = Photo.objects.filter(user=self.request.user).count()

        trails = Trail.objects.filter(trail_logs__in=context['trail_logs'],
                                      trail_logs__user=self.request.user).distinct()

        animals = Animal.objects.filter(trail_logs__user=self.request.user).distinct()

        context['animals_paginated'] = self.paginate_context(animals, 'page_animals', self.paginate_by)
        context['animals_page_param'] = 'page_animals'  # Pass the parameter name for animals pagination ('partials')

        # photos are not always related to a trail_log
        photos = Photo.objects.filter(user=self.request.user)
        context['photos_paginated'] = self.paginate_context(photos, 'page_photos', self.paginate_by)
        context['photos_page_param'] = 'page_photos'  # Pass the parameter name for photos pagination ('partials')

        context['total_trails'] = total_trails
        context['total_length'] = total_length
        context['total_species_seen'] = total_species_seen
        context['trail_logs_count'] = trail_logs_count
        context['trails'] = trails
        context['photos_count'] = photos_count

        return context

    def get_template_names(self):
        if 'trails' in self.request.path:
            return 'trail_logs/trail-logs-trails-page.html'
        elif 'animals' in self.request.path:
            return 'trail_logs/trail-logs-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail-logs-photos-page.html'
        else:
            return self.template_name


class TrailLogSpecificTrailView(ListView):
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 3
    template_name = 'trail_logs/trail-logs-specific-trail-logs-page.html'

    def get_queryset(self):
        trail_id = self.kwargs.get('trail_id')
        return TrailLog.objects.filter(
            user=self.request.user,
            trail_id=trail_id,
        ).select_related('trail') \
            .prefetch_related('animals', 'photos') \
            .order_by('-date_completed')

    def paginate_context(self, queryset, page_param, per_page):
        page_number = self.request.GET.get(page_param, 1)
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page_number)

    # TODO move to a different file to use across all CBV

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trail_id = self.kwargs.get('trail_id')
        trail = get_object_or_404(Trail, pk=trail_id)
        context['trail'] = trail

        # Paginate photos
        photos = Photo.objects.filter(trail_id=trail_id, user=self.request.user).distinct()
        context['photos_paginated'] = self.paginate_context(photos, 'page_photos', self.paginate_by)
        context['photos_page_param'] = 'page_photos'  # Pass the parameter name for photos pagination ('partials')

        # Paginate animals
        animals = Animal.objects.filter(trail_logs__in=context['trail_logs']).distinct()
        context['animals_paginated'] = self.paginate_context(animals, 'page_animals', self.paginate_by)
        context['animals_page_param'] = 'page_animals'  # Pass the parameter name for animals pagination ('partials')

        # TODO add total_logs to context. It counts the logs per page now

        return context

    def get_template_names(self):
        if 'animals' in self.request.path:
            return 'trail_logs/trail-logs-specific-trail-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail-logs-specific-trail-photos-page.html'
        else:
            return self.template_name


class TrailLogSpecificAnimalView(ListView):  # every time the user logged this animal
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 3
    template_name = 'trail_logs/trail-logs-specific-animal-logs-page.html'

    def get_queryset(self):
        animal_id = self.kwargs['animal_id']
        return TrailLog.objects.filter(
            animals__id=animal_id,
            user=self.request.user
        ).select_related('trail').prefetch_related('photos', 'animals')

    def paginate_context(self, queryset, page_param, per_page):
        page_number = self.request.GET.get(page_param, 1)
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = get_object_or_404(Animal, id=self.kwargs['animal_id'])

        context['animal'] = animal
        context['trails'] = Trail.objects.filter(trail_logs__in=context['trail_logs']).distinct()

        photos = Photo.objects.filter(animal=animal, user=self.request.user)
        context['photos_paginated'] = self.paginate_context(photos, 'page_photos', self.paginate_by)
        context['photos_page_param'] = 'page_photos'  # Pass the parameter name for photos pagination ('partials')

        return context

    def get_template_names(self):
        if 'trails' in self.request.path:
            return 'trail_logs/trail-logs-specific-animal-trails-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail-logs-specific-animal-photos-page.html'
        else:
            return self.template_name


class TrailLogEditView(UpdateView):
    model = TrailLog
    form_class = TrailLogEditForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-edit-page.html'

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.animals.set(form.cleaned_data['animals_spotted'])
        return response

    def get_success_url(self):
        return reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.object.pk})


class TrailLogDeleteView(DeleteView):
    model = TrailLog
    form_class = TrailLogDeleteForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-delete-page.html'
    success_url = reverse_lazy('trail-logs-list')

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail')

    def get_initial(self):
        return self.object.__dict__
