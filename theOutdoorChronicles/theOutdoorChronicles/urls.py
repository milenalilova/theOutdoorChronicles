from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theOutdoorChronicles.common.urls')),
    path('accounts/', include('theOutdoorChronicles.accounts.urls')),
    path('trails/', include('theOutdoorChronicles.trails.urls')),
    path('animals/', include('theOutdoorChronicles.animals.urls')),
    path('photos/', include('theOutdoorChronicles.photos.urls')),
    path('trail-logs/', include('theOutdoorChronicles.trail_logs.urls')),
    path('maps/', include('theOutdoorChronicles.maps.urls')),
    path('weather/', include('theOutdoorChronicles.weather.urls')),
]

handler403 = 'theOutdoorChronicles.common.views.custom_403'
handler404 = 'theOutdoorChronicles.common.views.custom_404'

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
