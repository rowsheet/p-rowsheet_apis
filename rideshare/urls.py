import os
from django.urls import path
from rideshare import views
from django.conf import settings
from django.urls import path, include

if settings.DEPLOYMENT_MODE == "PRODUCTION":
    """
    This is the old landing page.
    """
    urlpatterns = [
        # Site pages.
        path("", views.index),
        path("for-drivers/", views.for_drivers),
        path("for-riders/", views.for_riders),
        path("why-homobiles/", views.why_homobiles),
        path("signup/", views.signup),
    ]
else:
    """
    This is the new fancy app.
    """
    urlpatterns = [
        # On-boarding pages.
        path("", views.get_started),
        path("phone_verification/", views.phone_verification),
        path("code_verification/", views.code_verification),
        #-----------------------------------------------------------------------
        #   PASSENGER
        #-----------------------------------------------------------------------
        # Main pages.
        path("main_screen/", views.main_screen),
        path("set_location/", views.set_location),
        path("account/", views.account),
        path("profile/", views.profile),
        # Sidebar pages
        path("past_rides/", views.past_rides),
        path("upcoming_rides/", views.upcoming_rides),
        path("donation_station/", views.donation_station),
        path("settings/", views._settings),
        path("driver/", views.driver),
        path("about/", views.about),
        path("help/", views.help),
        # Account pages.
        path("payment_methods/", views.payment_methods),
        path("email_address/", views.email_address),
        path("phone_number/", views.phone_number),
        # Settings pages.
        path("services/", views.services),
        path("location/", views.location),
        path("notifications/", views.notifications),
        path("emergency/", views.emergency),
        path("trusted_contacts/", views.trusted_contacts),
        path("delete_account/", views.delete_account),
        # Help pages.
        path("report_a_recent_ride/", views.report_a_recent_ride),
        path("report_a_lost_item/", views.report_a_lost_item),
        path("how_ride_payment_works/", views.how_ride_payment_works),
        path("free_rides/", views.free_rides),
        path("saftey/", views.saftey),
        path("policies/", views.policies),
        path("legal/", views.legal),
        #-----------------------------------------------------------------------
        #   DRIVER
        #-----------------------------------------------------------------------
        path("driver/past_rides/", views.driver_past_rides),
        path("driver/upcoming_rides/", views.driver_upcoming_rides),
        path("driver/available_rides/", views.driver_available_rides),
        path("driver/notifications/", views.driver_notifications),
        path("driver/account/", views.driver_account),
        path("driver/settings/", views.driver_settings),
        path("driver/about/", views.driver_about),
        path("driver/help/", views.driver_help),
        # Driver /account/
        path("driver/profile/", views.driver_profile),
        path("driver/payment_methods/", views.driver_payment_methods),
        path("driver/email_address/", views.driver_email_address),
        path("driver/phone_number/", views.driver_phone_number),
        path("driver/services/", views.driver_services),
        #-----------TEMP-----------
        # DEMO
        path("demo_google_maps/", views.demo_google_maps),
        path("geocode/", views.geocode),
        path("api/", include("rideshare.api")),
    ]
