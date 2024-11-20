from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.trail_logs.forms import TrailLogCreateForm, TrailLogEditForm, TrailLogDeleteForm
from theOutdoorChronicles.trail_logs.models import TrailLog


class TrailLogCreateView(CreateView):
    model = TrailLog
    form_class = TrailLogCreateForm
    pk_url_kwarg = 'trail_log_id'
    template_name = 'trail_logs/trail-log-create-page.html'

    def form_valid(self, form):
        log = form.save(commit=False)
        log.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trail-log-details', kwargs={'trail_log_id': self.object.pk})


#     TODO refactor to get user.pk from url
#     TODO hide fields trail and photos from the form


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
