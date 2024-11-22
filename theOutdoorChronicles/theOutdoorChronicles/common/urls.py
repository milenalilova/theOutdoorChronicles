from django.urls import path

from theOutdoorChronicles.common import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home-page'),
    path('about/', views.AboutView.as_view(), name='about-page'),
]
