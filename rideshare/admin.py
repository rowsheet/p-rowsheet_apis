from django.contrib import admin

from .models import AppUser
from .models import Pronoun
from .models import Accommodation
from .models import RideRequest


class RideRequestAdmin(admin.ModelAdmin):
    fields = (
        "start_name",
        "start_address",
        "start_place_id",
        "end_name",
        "end_address",
        "end_place_id",
        "ride_utc",
        "csrf_token",
    )
    list_display = fields
    search_fields = fields


admin.site.register(RideRequest, RideRequestAdmin)


class PronounAdmin(admin.ModelAdmin):
    fields = (
        "key",
        "display_name",
    )
    list_display = fields
    search_fields = fields


admin.site.register(Pronoun, PronounAdmin)


class AccommodationAdmin(admin.ModelAdmin):
    fields = (
        "key",
        "display_name",
    )
    list_display = fields
    search_fields = fields


admin.site.register(Accommodation, AccommodationAdmin)


class AppUserAdmin(admin.ModelAdmin):
    list_display = (
        "django_account",
        "username",
        "pronoun",
        "phone_number",
        "phone_verified",
        "get_accommodations",
    )
    search_fields = (
        "django_account",
        "username",
        "pronoun",
        "phone_number",
        "phone_verified",
    )


admin.site.register(AppUser, AppUserAdmin)
