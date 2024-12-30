from django.urls import path

from theOutdoorChronicles.weather import views

urlpatterns = [
    path('', views.WeatherView.as_view(), name='weather-page'),
]
