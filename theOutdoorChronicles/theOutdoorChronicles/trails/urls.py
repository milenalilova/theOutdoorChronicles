from django.urls import path, include

from theOutdoorChronicles.trails import views
from theOutdoorChronicles.photos import views as photos_views

urlpatterns = [
    path('create/', views.TrailCreateView.as_view(), name='trail-create'),
    path('explore/', views.TrailListView.as_view(), name='trail-list'),
    path('<int:trail_id>/', include([
        path('details/', include([
            path('', views.TrailDetailsView.as_view(), name='trail-details'),
            path('animals/', views.TrailDetailsView.as_view(), name='trail-details-animals'),
            path('photos/', views.TrailDetailsView.as_view(), name='trail-details-photos'),
            path('trail-logs/', views.TrailDetailsView.as_view(), name='trail-details-trail-logs'),
        ])),
        path('edit/', views.TrailEditView.as_view(), name='trail-edit'),
        path('delete/', views.TrailDeleteView.as_view(), name='trail-delete'),
        path('upload-photo/', photos_views.PhotoCreateView.as_view(), name='trail-photo-upload')
    ])),
]

