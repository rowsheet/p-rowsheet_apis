from django.contrib import admin

from .models import AppUser
from .models import Pronoun
from .models import Accommodation
from .models import RideRequest
from .models import OldRideRequest
from .models import OldDriverSignup


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


class OldRideRequestAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "end_location",
        "start_location",
        "phone_number",
        "pickup_time",
        "pickup_date",
        "pronoun",
        "special_req",
        "num_bags",
        "passenger_count",
        "driver",
        "done",
        "creation_timestamp",
    )
    list_display = fields
    search_fields = fields
    readonly_fields = (
        "creation_timestamp",
    )


admin.site.register(OldRideRequest, OldRideRequestAdmin)


class OldDriverSignupAdmin(admin.ModelAdmin):
    fields = (
        "contact_email",
        "contact_phone",
        "first_name",
        "last_name",
        "pronoun",
        "smartphone_type",
        "vehicle_doors",
        "vehicle_make",
        "vehicle_model",
        "vehicle_year",
        "yes_no_criminal_history",
        "yes_no_insurance",
        "yes_no_square",
        "comments",
        "creation_timestamp",
    )
    list_display = fields
    search_fields = fields
    readonly_fields = (
        "creation_timestamp",
    )


admin.site.register(OldDriverSignup, OldDriverSignupAdmin)
