from django.urls import path, include

from theOutdoorChronicles.trail_logs import views

urlpatterns = [
    path('create/', views.TrailLogCreateView.as_view(), name='trail-log-create'),
    path('explore/', views.TrailLogListView.as_view(), name='trail-log-list'),
    path('<int:trail_log_id>/', include([
        path('details/', views.TrailLogDetailsView.as_view(), name='trail-log-details'),
        path('edit/', views.TrailLogEditView.as_view(), name='trail-log-edit'),
        path('delete/', views.TrailLogDeleteView.as_view(), name='trail-log-delete')
    ])),
]
