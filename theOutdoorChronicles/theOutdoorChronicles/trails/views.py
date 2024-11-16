from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from theOutdoorChronicles.trails.forms import TrailCreateForm, TrailEditForm, TrailDeleteForm
from theOutdoorChronicles.trails.models import Trail


class TrailCreateView(CreateView):
    model = Trail
    form_class = TrailCreateForm
    template_name = 'trails/trail-create-page.html'
    pk_url_kwarg = 'trail_id'

    def get_success_url(self):
        return reverse_lazy('trail-details', kwargs={'trail_id': self.object.pk})


class TrailDetailsView(DetailView):
    model = Trail
    template_name = 'trails/trail-details-page.html'
    pk_url_kwarg = 'trail_id'


class TrailListView(ListView):
    model = Trail
    template_name = 'trails/trail-list-page.html'
    context_object_name = 'trails'


class TrailEditView(UpdateView):
    model = Trail
    form_class = TrailEditForm
    template_name = 'trails/trail-edit-page.html'
    pk_url_kwarg = 'trail_id'

    def get_success_url(self):
        return reverse_lazy('trail-details', kwargs={'trail_id': self.object.pk})


class TrailDeleteView(DeleteView):
    model = Trail
    form_class = TrailDeleteForm
    template_name = 'trails/trail-delete-page.html'
    success_url = reverse_lazy('trail-list')
    pk_url_kwarg = 'trail_id'

    def get_initial(self):
        return self.object.__dict__
