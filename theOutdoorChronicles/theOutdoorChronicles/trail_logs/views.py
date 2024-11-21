from django import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.trail_logs.forms import TrailLogCreateForm, TrailLogEditForm, TrailLogDeleteForm
from theOutdoorChronicles.trail_logs.models import TrailLog
from theOutdoorChronicles.trails.models import Trail


class TrailLogCreateView(CreateView):
    model = TrailLog
    form_class = TrailLogCreateForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-create-page.html'

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


class TrailLogListView(ListView):
    model = TrailLog
    context_object_name = 'trail_logs'
    paginate_by = 5
    template_name = 'trail_logs/trail-log-list-page.html'


class TrailLogEditView(UpdateView):
    model = TrailLog
    form_class = TrailLogEditForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.object.pk})


class TrailLogDeleteView(DeleteView):
    model = TrailLog
    form_class = TrailLogDeleteForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-delete-page.html'
    success_url = reverse_lazy('trail-log-list')

    def get_initial(self):
        return self.object.__dict__
