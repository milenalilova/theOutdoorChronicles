from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.animals.models import Animal
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

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail')


# TODO add next and previous log, or go back to all logs
# TODO check the queryset
# TODO after photo upload,after redirect, option to go back to photo uploads

class TrailLogListView(ListView):  # all hiking user experience
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 5
    template_name = 'trail_logs/trail-log-list-page.html'

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

        # uses reverse relation from Trail
        total_length = Trail.objects.filter(trail_logs__user=self.request.user) \
                           .aggregate(total_length=Sum('length'))['total_length'] or 0

        # uses reverse relation from Animal
        total_species_seen = Animal.objects.filter(trail_logs__user=self.request.user) \
            .distinct() \
            .count()

        context['total_trails'] = total_trails
        context['total_length'] = total_length
        context['total_species_seen'] = total_species_seen

        return context


#  TODO use animals and photos from get_queryset

class TrailLogSpecificTrailView(ListView):  # every time the user hiked this trail
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 5
    template_name = 'trail_logs/trail-log-specific-trail-page.html'

    def get_queryset(self):
        trail_id = self.kwargs.get('trail_id')

        return TrailLog.objects.filter(
            user=self.request.user,
            trail_id=trail_id,
        ).select_related('trail').order_by('-date_completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trail_id = self.kwargs.get('trail_id')
        trail = get_object_or_404(Trail, pk=trail_id)
        context['trail'] = trail

        return context


# TODO create the same for Trail. Think about one view for both.


class TrailLogEditView(UpdateView):
    model = TrailLog
    form_class = TrailLogEditForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-edit-page.html'

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail')

    def get_success_url(self):
        return reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.object.pk})


class TrailLogDeleteView(DeleteView):
    model = TrailLog
    form_class = TrailLogDeleteForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-delete-page.html'
    success_url = reverse_lazy('trail-log-list')

    def get_queryset(self):
        return TrailLog.objects.filter(user=self.request.user) \
            .select_related('trail')

    def get_initial(self):
        return self.object.__dict__

#  TODO remove animals field from delete form or display as a readonly list
