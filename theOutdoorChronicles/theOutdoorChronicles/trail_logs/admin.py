from django.contrib import admin

from theOutdoorChronicles.trail_logs.models import TrailLog


@admin.register(TrailLog)
class TrailLogAdmin(admin.ModelAdmin):
    list_display = ('date_completed', 'title', 'user')
    search_fields = ('date_completed', 'title',)
    ordering = ('date_completed','user')
