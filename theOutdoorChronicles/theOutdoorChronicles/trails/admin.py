from django.contrib import admin

from theOutdoorChronicles.trails.models import Trail


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'length', 'difficulty')
    list_filter = ('name', 'location', 'difficulty')
    search_fields = ('name', 'location', 'difficulty')
    ordering = ('location',)
