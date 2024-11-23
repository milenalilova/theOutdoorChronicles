from django.urls import path, include

from theOutdoorChronicles.trail_logs import views
from theOutdoorChronicles.photos import views as photos_views

urlpatterns = [
    path('create/<int:trail_id>/', views.TrailLogCreateView.as_view(), name='trail-log-create'),
    # create gets a trail_id to log experience on that particular trail
    path('explore/', views.TrailLogListView.as_view(), name='trail-log-list'),
    path('explore/<int:trail_id>', views.TrailLogSpecificTrailView.as_view(), name='trail-log-specific-trail'),
    path('<int:trail_log_id>/', include([
        path('details/', views.TrailLogDetailsView.as_view(), name='trail-log-details'),
        path('edit/', views.TrailLogEditView.as_view(), name='trail-log-edit'),
        path('delete/', views.TrailLogDeleteView.as_view(), name='trail-log-delete'),
        path('upload-photo/', photos_views.PhotoCreateView.as_view(), name='trail-log-photo-upload')

    ])),
]

# TODO possibly add slugs
