import os
from django.urls import path
from rideshare import views
from django.conf import settings

"""
Since Homobiles has the "old" active production pages, set these as the
active url route if no other "DEPLOYMENT_MODE" is set.
For development, add something other than "PRODUCTION" for the "DEPLOYMENT_MODE"
in the .env file.
"""
if settings.DEPLOYMENT_MODE == "PRODUCTION":
    urlpatterns = [
        # Site pages.
        path("", views.index),
        path("for-drivers/", views.for_drivers),
        path("for-riders/", views.for_riders),
        path("why-homobiles/", views.why_homobiles),
        path("signup/", views.signup),
    ]
else:
    urlpatterns = [
        # DEMO
        path("demo_google_maps/", views.demo_google_maps),
        # On-boarding pages.
        # path("get_started/", views.get_started),
        path("", views.get_started),
        path("phone_verification/", views.phone_verification),
        path("code_verification/", views.code_verification),
        # Main pages.
        path("main_screen/", views.main_screen),
        path("set_location/", views.set_location),
        path("account/", views.account),
        path("profile/", views.profile),
        # Sidebar pages
        path("past_rides/", views.past_rides),
        path("donation_station/", views.donation_station),
        path("settings/", views.settings),
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
    ]
