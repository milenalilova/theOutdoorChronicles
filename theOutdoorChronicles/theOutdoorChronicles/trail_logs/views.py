from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.common.utils import paginate_and_add_to_context
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


class TrailLogDetailsView(LoginRequiredMixin, DetailView):
    model = TrailLog
    context_object_name = 'trail_log'
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail_log_details/trail-log-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = self.object.animals.all()
        context['photos'] = self.object.photos.all()
        return context

    def get_queryset(self):
        return TrailLog.objects.select_related('trail').prefetch_related('animals', 'photos')

    def get_template_names(self):
        if 'animals' in self.request.path:
            return 'trail_logs/trail_log_details/trail-log-details-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail_log_details/trail-log-details-photos-page.html'
        else:
            return self.template_name


class TrailLogListView(LoginRequiredMixin, ListView):  # All hiking user experience
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 3
    template_name = 'trail_logs/trail_logs_my_logs/trail-logs-my-logs.html'

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail') \
            .prefetch_related('animals', 'photos') \
            .order_by('-date_completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_trails = TrailLog.objects.filter(user=self.request.user) \
            .values('trail') \
            .distinct() \
            .count()

        # Uses reverse relation from Trail
        total_length = Trail.objects.filter(trail_logs__user=self.request.user) \
                           .aggregate(total_length=Sum('length'))['total_length'] or 0

        # Uses reverse relation from Animal
        total_species_seen = Animal.objects.filter(trail_logs__user=self.request.user) \
            .distinct() \
            .count()

        trail_logs_count = self.get_queryset().count()
        photos_count = Photo.objects.filter(user=self.request.user).count()

        trails = Trail.objects.filter(trail_logs__user=self.request.user).distinct()
        context = paginate_and_add_to_context(trails, context, 'trail', self.paginate_by, self.request)

        animals = Animal.objects.filter(trail_logs__user=self.request.user).distinct()
        context = paginate_and_add_to_context(animals, context, 'animal', self.paginate_by, self.request)

        # photos are not always related to a trail_log
        photos = Photo.objects.filter(user=self.request.user)
        context = paginate_and_add_to_context(photos, context, 'photo', self.paginate_by, self.request)

        context['total_trails'] = total_trails
        context['total_length'] = total_length
        context['total_species_seen'] = total_species_seen
        context['trail_logs_count'] = trail_logs_count
        context['photos_count'] = photos_count

        return context

    def get_template_names(self):
        if 'trails' in self.request.path:
            return 'trail_logs/trail_logs_my_logs/trail-logs-my-trails-page.html'
        elif 'animals' in self.request.path:
            return 'trail_logs/trail_logs_my_logs/trail-logs-my-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail_logs_my_logs/trail-logs-my-photos-page.html'
        else:
            return self.template_name


class TrailLogSpecificTrailView(LoginRequiredMixin, ListView):
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 3
    template_name = 'trail_logs/trail_logs_specific_trail_logs/trail-logs-specific-trail-logs-page.html'

    def get_queryset(self):
        trail_id = self.kwargs.get('trail_id')
        return TrailLog.objects.filter(
            user=self.request.user,
            trail_id=trail_id,
        ).select_related('trail') \
            .prefetch_related('animals', 'photos') \
            .order_by('-date_completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trail_id = self.kwargs.get('trail_id')
        trail = get_object_or_404(Trail, pk=trail_id)
        context['trail'] = trail

        context['trail_logs_count'] = self.get_queryset().count()

        # Paginate photos
        photos = Photo.objects.filter(trail_id=trail_id, user=self.request.user).distinct()
        context['photos_count'] = photos.count()
        context = paginate_and_add_to_context(photos, context, 'photo', self.paginate_by, self.request)

        # Paginate animals
        animals = Animal.objects.filter(trail_logs__in=context['trail_logs']).distinct()
        context['animals_count'] = animals.count()
        context = paginate_and_add_to_context(animals, context, 'animal', self.paginate_by, self.request)

        return context

    def get_template_names(self):
        if 'animals' in self.request.path:
            return 'trail_logs/trail_logs_specific_trail_logs/trail-logs-specific-trail-animals-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail_logs_specific_trail_logs/trail-logs-specific-trail-photos-page.html'
        else:
            return self.template_name


class TrailLogSpecificAnimalView(LoginRequiredMixin, ListView):  # every time the user logged this animal
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 3
    template_name = 'trail_logs/trail_logs_specific_animal_logs/trail-logs-specific-animal-logs-page.html'

    def get_queryset(self):
        animal_id = self.kwargs['animal_id']
        return TrailLog.objects.filter(
            animals__id=animal_id,
            user=self.request.user
        ).select_related('trail').prefetch_related('photos', 'animals')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        animal = get_object_or_404(Animal, id=self.kwargs['animal_id'])
        context['animal'] = animal

        trails = Trail.objects.filter(trail_logs__in=context['trail_logs']).distinct()
        context['trails'] = trails
        context['trails_count'] = trails.count()

        photos = Photo.objects.filter(animal=animal, user=self.request.user)
        context['photos_count'] = photos.count()
        context = paginate_and_add_to_context(photos, context, 'photo', self.paginate_by, self.request)

        return context

    def get_template_names(self):
        if 'trails' in self.request.path:
            return 'trail_logs/trail_logs_specific_animal_logs/trail-logs-specific-animal-trails-page.html'
        elif 'photos' in self.request.path:
            return 'trail_logs/trail_logs_specific_animal_logs/trail-logs-specific-animal-photos-page.html'
        else:
            return self.template_name


class TrailLogEditView(LoginRequiredMixin, UpdateView):
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
        form.instance.photos.set(form.cleaned_data['photos_uploaded'])
        return response

    def get_success_url(self):
        return reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.object.pk})


class TrailLogDeleteView(LoginRequiredMixin, DeleteView):
    model = TrailLog
    form_class = TrailLogDeleteForm
    pk_url_kwarg = 'trail_log_id'
    context_object_name = 'trail_log'
    template_name = 'trail_logs/trail-log-delete-page.html'
    success_url = reverse_lazy('trail-logs-my-logs')

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals_spotted'] = self.object.animals.all()
        context['photos_uploaded'] = self.object.photos.all()
        return context

    def get_initial(self):
        return self.object.__dict__
