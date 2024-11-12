from django.contrib import admin

from theOutdoorChronicles.accounts.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass
