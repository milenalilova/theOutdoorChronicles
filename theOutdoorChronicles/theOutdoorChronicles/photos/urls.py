from django.urls import path, include

from theOutdoorChronicles import photos
from theOutdoorChronicles.photos import views

urlpatterns = [
    path('create/', views.PhotoCreateView.as_view(), name='photo-create'),
    path('explore/', views.PhotoListView.as_view(), name='photo-list'),
    path('<int:photo_id>/', include([
        path('details/', views.PhotoDetailView.as_view(), name='photo-details'),
        path('edit/', views.PhotoEditView.as_view(), name='photo-edit'),
        path('delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
    ])),
]
