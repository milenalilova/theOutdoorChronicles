from django.urls import path, include

from theOutdoorChronicles.trail_logs import views
from theOutdoorChronicles.photos import views as photos_views

urlpatterns = [
    path('create/<int:trail_id>/', views.TrailLogCreateView.as_view(), name='trail-log-create'),
    # create gets a trail_id to log experience on that particular trail
    path('explore/', include([
        path('', views.TrailLogListView.as_view(), name='trail-log-list'),

        path('trail/<int:trail_id>/', include([
            path('logs/', views.TrailLogSpecificTrailView.as_view(), name='trail-logs-specific-trail-logs'),
            path('animals/', views.TrailLogSpecificTrailView.as_view(), name='trail-logs-specific-trail-animals'),
            path('photos/', views.TrailLogSpecificTrailView.as_view(), name='trail-logs-specific-trail-photos'),
        ])),
        path('animal/<int:animal_id>/', include([
            path('logs/',views.TrailLogSpecificAnimalView.as_view(), name='trail-logs-specific-animal-logs' ),
            path('trails/',views.TrailLogSpecificAnimalView.as_view(), name='trail-logs-specific-animal-trails' ),
            path('photos/',views.TrailLogSpecificAnimalView.as_view(), name='trail-logs-specific-animal-photos' )
        ])),
        path('<int:trail_log_id>/', include([
            path('details/', include([
                path('', views.TrailLogDetailsView.as_view(), name='trail-log-details'),
                path('animals/', views.TrailLogDetailsView.as_view(), name='trail-log-details-animals'),
                path('photos/', views.TrailLogDetailsView.as_view(), name='trail-log-details-photos'),
            ])),
            path('edit/', views.TrailLogEditView.as_view(), name='trail-log-edit'),
            path('delete/', views.TrailLogDeleteView.as_view(), name='trail-log-delete'),
            path('upload-photo/', photos_views.PhotoCreateView.as_view(), name='trail-log-photo-upload')

        ])),
    ])),
]
# TODO improve urls readability
# TODO possibly add slugs

# urlpatterns = [
#     path('create/<int:trail_id>/', views.TrailLogCreateView.as_view(), name='trail-log-create'),
#     # create gets a trail_id to log experience on that particular trail
#     path('explore/', views.TrailLogListView.as_view(), name='trail-log-list'),
#     path('explore/<int:trail_id>/', include([
#         path('', views.TrailLogSpecificTrailView.as_view(), name='trail-log-specific-trail-list'),
#         path('animals/', views.TrailLogSpecificTrailView.as_view(), name='trail-log-specific-trail-animals'),
#         path('photos/', views.TrailLogSpecificTrailView.as_view(), name='trail-log-specific-trail-photos'),
#     ])),
#     path('<int:trail_log_id>/', include([
#         path('details/', include([
#             path('', views.TrailLogDetailsView.as_view(), name='trail-log-details'),
#             path('animals/', views.TrailLogDetailsView.as_view(), name='trail-log-details-animals'),
#             path('photos/', views.TrailLogDetailsView.as_view(), name='trail-log-details-photos'),
#         ])),
#         path('edit/', views.TrailLogEditView.as_view(), name='trail-log-edit'),
#         path('delete/', views.TrailLogDeleteView.as_view(), name='trail-log-delete'),
#         path('upload-photo/', photos_views.PhotoCreateView.as_view(), name='trail-log-photo-upload')
#
#     ])),
# ]
