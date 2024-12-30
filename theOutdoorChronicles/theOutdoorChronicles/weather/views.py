from django.conf import settings
from django.views.generic import TemplateView

from theOutdoorChronicles.weather.utils import get_weather


class WeatherView(TemplateView):
    template_name = 'weather/weather-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city', 'Cayenne')
        api_key = settings.WEATHER_API_KEY
        weather_data = get_weather(city, api_key)

        context['weather_data'] = weather_data
        context['city'] = city

        return context
