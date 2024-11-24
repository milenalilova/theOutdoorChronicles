from django.views.generic import TemplateView


class MapView(TemplateView):
    template_name = 'maps/map-page.html'
