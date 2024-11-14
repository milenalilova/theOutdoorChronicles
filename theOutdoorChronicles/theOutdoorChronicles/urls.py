from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theOutdoorChronicles.common.urls')),
    path('accounts/', include('theOutdoorChronicles.accounts.urls')),
    path('trails/', include('theOutdoorChronicles.trails.urls')),
    path('animals/', include('theOutdoorChronicles.animals.urls')),
    path('photos/', include('theOutdoorChronicles.photos.urls')),
]
