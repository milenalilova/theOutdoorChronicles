from django.urls import path, include

from theOutdoorChronicles.animals import views
from theOutdoorChronicles.photos import views as photos_views

urlpatterns = [
    path('create/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('explore/', views.AnimalListView.as_view(), name='animal-list'),
    path('<int:animal_id>/', include([
        path('details/', include([
            path('', views.AnimalDetailsView.as_view(), name='animal-details'),
            path('trails/', views.AnimalDetailsView.as_view(), name='animal-details-trails'),
            path('photos/', views.AnimalDetailsView.as_view(), name='animal-details-photos'),
            path('trail-logs/', views.AnimalDetailsView.as_view(), name='animal-details-trail-logs')
        ])),
        path('edit/', views.AnimalEditView.as_view(), name='animal-edit'),
        path('delete/', views.AnimalDeleteView.as_view(), name='animal-delete'),
        path('upload-photo/', photos_views.PhotoCreateView.as_view(), name='animals-photo-upload')
    ])),
]

# TODO possibly add slugs
