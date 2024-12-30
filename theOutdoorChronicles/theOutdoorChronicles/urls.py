from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
