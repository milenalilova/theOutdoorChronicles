from django.contrib import admin

from theOutdoorChronicles.photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('trail', 'date_uploaded', 'user',)
    list_filter = ('date_uploaded', 'trail')
    search_fields = ('date_uploaded', 'trail',)
