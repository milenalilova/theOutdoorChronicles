from django.urls import path

from theOutdoorChronicles.maps import views

urlpatterns = [
    path('', views.MapView.as_view(), name='map-page'),
]
