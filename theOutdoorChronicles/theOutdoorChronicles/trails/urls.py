from django.urls import path, include

from theOutdoorChronicles import trails
from theOutdoorChronicles.trails import views

urlpatterns = [
    path('create/', views.TrailCreateView.as_view(), name='trail-create'),
    path('explore/', views.TrailListView.as_view(), name='trail-list'),
    path('<int:trail_id>/', include([
        path('details/', views.TrailDetailsView.as_view(), name='trail-details'),
        path('edit/', views.TrailEditView.as_view(), name='trail-edit'),
        path('delete/', views.TrailDeleteView.as_view(), name='trail-delete')
    ])),
]
