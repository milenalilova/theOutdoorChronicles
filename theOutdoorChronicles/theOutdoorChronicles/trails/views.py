from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from theOutdoorChronicles.trails.forms import TrailCreateForm, TrailEditForm, TrailDeleteForm
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
    template_name = 'trails/trail-details-page.html'


#     TODO add a list of animals often found on the trail to the context


class TrailListView(ListView):
    model = Trail
    context_object_name = 'trails'
    paginate_by = 3
    template_name = 'trails/trail-list-page.html'


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

    def get_initial(self):
        return self.object.__dict__


