from django.urls import path, include

from theOutdoorChronicles import animals
from theOutdoorChronicles.animals import views

urlpatterns = [
    path('create/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('explore/', views.AnimalListView.as_view(), name='animal-list'),
    path('<int:animal_id>/', include([
        path('details/', views.AnimalDetailsView.as_view(), name='animal-details'),
        path('edit/', views.AnimalEditView.as_view(), name='animal-edit'),
        path('delete/', views.AnimalDeleteView.as_view(), name='animal-delete')
    ])),
]
