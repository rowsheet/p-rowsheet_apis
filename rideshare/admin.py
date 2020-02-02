from django.contrib import admin

from .models import AppUser
from .models import Pronoun
from .models import Accommodation
from .models import RideRequest


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
        "icon",
        "description",
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
        "phone_verification_code",
        "phone_verified",
        "email_address",
        "email_verification_code",
        "email_verified",
        # Synthetic
        "get_accommodations",
    )
    search_fields = (
        "django_account",
        "username",
        "pronoun",
        "phone_number",
        "phone_verified",
        "email_address",
        "email_verified",
    )


admin.site.register(AppUser, AppUserAdmin)


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
        "app_user",
        "creation_timestamp",
        "status",
    )
    list_display = fields
    search_fields = fields
    readonly_fields = (
        "creation_timestamp",
    )


admin.site.register(RideRequest, RideRequestAdmin)
