from django.contrib import admin

from theOutdoorChronicles.animals.models import Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('species', 'common_name', 'get_trails')
    list_filter = ('species', 'common_name',)
    search_fields = ('species', 'common_name')
    ordering = ('species',)

    def get_trails(self, obj):
        return ', '.join(trail.name for trail in obj.trails.all())

    get_trails.short_description = 'Found on Trails'
