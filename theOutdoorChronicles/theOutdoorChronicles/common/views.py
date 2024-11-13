from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from theOutdoorChronicles.accounts.models import Profile


class IndexView(TemplateView):
    template_name = 'common/home-page.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated:
    #         context['profile'] = get_object_or_404(Profile, user=self.request.user)
    #     return context

# TODO do I really need get_context_data here?
