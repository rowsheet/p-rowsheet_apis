import enum

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

import rowsheet.utils as rs_utils
from random import randrange

from datetime import datetime


class Pronoun(models.Model):
    class Meta:
        verbose_name= 'Pronoun'
        verbose_name_plural= 'Pronouns'
    key = models.CharField(
        unique=True,
        max_length=16,
        null=False, blank=False, default=None,
    )
    display_name = models.CharField(
        unique=True,
        max_length=32,
        null=False, blank=False, default=None,
    )

class Accommodation(models.Model):
    class Meta:
        verbose_name= 'Accomodation'
        verbose_name_plural= 'Accomodations'
    key = models.CharField(
        unique=True,
        max_length=16,
        null=False, blank=False, default=None,
    )
    display_name = models.CharField(
        unique=True,
        max_length=32,
        null=False, blank=False, default=None,
    )
    icon = models.CharField(
        unique=False,
        max_length=64,
        null=False, blank=False, default="",
    )
    description = models.CharField(
        unique=False,
        max_length=255,
        null=False, blank=False, default="",
    )
    def __str__(self):
        return str(self.display_name)


class AppUser(models.Model):
    class Meta:
        verbose_name= 'App User'
        verbose_name_plural= 'App Users'
    django_account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False, blank=False, default=None,
    )
    username = models.CharField(
        max_length=64,
        null=False, blank=False, default="Username Unset",
    )
    pronoun = models.ForeignKey(
        Pronoun,
        on_delete=models.PROTECT,  # same as RESTRICT
        null=True, blank=True, default=1,
    )
    phone_number = models.CharField(
        max_length=32,
        null=True, blank=True, default=None,
    )
    phone_verification_code = models.CharField(
        max_length=32,
        null=False, blank=False, default=rs_utils.random_phone_code,
    )
    phone_verified = models.BooleanField(
        default=False,
        null=False, blank=False,
    )
    accommodations = models.ManyToManyField(
        Accommodation
    )
    email_address = models.CharField(
        max_length=64,
        null=True, blank=True, default=None,
        unique=True,
    )
    email_verification_code = models.CharField(
        max_length=100,
        null=False, blank=False, default=rs_utils.random_string(64),
    )
    email_verified = models.BooleanField(
        default=False,
        null=False, blank=False,
    )
    driver_approved = models.BooleanField(
        default=False,
        null=False, blank=False,
    )

    def get_accommodations(self):
        return ",".join([str(acc) for acc in self.accommodations.all()])

    def __str__(self):
        return "%s (%s) " % (
                str(self.django_account),
                str(self.username),
        )


class DonationSubscription(models.Model):
    app_user = models.ForeignKey(
        AppUser,
        on_delete=models.PROTECT,
        null=False, blank=False, default=None,
    )
    plan_id = models.CharField(
        max_length=500,
        null=False, blank=False, default=None,
    )
    product_id = models.CharField(
        max_length=500,
        null=False, blank=False, default=None,
    )
    checkout_session_id = models.CharField(
        max_length=500,
        null=False, blank=False, default=None,
    )
    subscription_id = models.CharField(
        max_length=500,
        null=True, blank=True, default=None,
    )
    amount = models.IntegerField(
        null=True, blank=True, default=None
    )
    currency = models.CharField(
        max_length=32,
        null=True, blank=True, default=None
    )
    interval = models.CharField(
        max_length=32,
        null=True, blank=True, default=None
    )
    success = models.BooleanField(
        null=True, blank=True, default=False
    )
    deleted = models.BooleanField(
        null=True, blank=True, default=False
    )
    creation_timestamp = models.DateTimeField(
        auto_now=True)

    def find_by_checkout_session_id(checkout_session_id):
        donation_subscription = DonationSubscription.objects.get(
            checkout_session_id=checkout_session_id,
        )
        return donation_subscription

    def print_summary(self):
        return """
        <div class="alert alert-secondary">
            <div class="row">
                <div class="col-6">
                    <small>
                        <p class="m-0">
                            <strong>
                                Amount:
                            </strong> {amount}
                        </p>
                        <p class="m-0">
                            <strong>
                                Currency:
                            </strong> {currency}
                        </p>
                        <p class="m-0">
                            <strong>
                                Interval:
                            </strong> {interval}
                        </p>
                        <p class="m-0">
                            <strong>
                                ID:
                            </strong> {subscription_id}
                        </p>
                    </small>
                </div>
                <div class="col-6 text-right">
                    <button class="btn btn-sm btn-danger"
                        onclick="cancel_subscription_by_subscription_id('{subscription_id}')">
                        Cancel Subscription
                    </button>
                </div>
            </div>
        </div>
        """.format(
            amount="%.2f" % (float(self.amount) / 100.0),
            currency=self.currency,
            interval=self.interval,
            subscription_id=self.subscription_id,
        )


class RideRequest(models.Model):
    class Meta:
        verbose_name = 'Rider Request (development)'
        verbose_name_plural = 'Rider Requests (development)'
        unique_together = ("app_user", "in_setup")
    start_address = models.CharField(
        unique=False,
        max_length=128,
        null=False, blank=False, default=None,
    )
    start_place_id = models.CharField(
        unique=False,
        max_length=256,
        null=False, blank=False, default=None,
    )
    end_address = models.CharField(
        unique=False,
        max_length=128,
        null=False, blank=False, default=None,
    )
    end_place_id = models.CharField(
        unique=False,
        max_length=256,
        null=False, blank=False, default=None,
    )
    app_user = models.ForeignKey(
        AppUser,
        on_delete=models.PROTECT,
        null=False, blank=False, default=None,
        # Note: unique cannot be true because we may use this for
        # batch processing and if the batch time is shorter than the
        # time in between the same users rides, the second ride attempt
        # will be impossible until that batch is run.
        # unique=True,
    )
    app_user_driver = models.ForeignKey(
        AppUser,
        on_delete=models.PROTECT,
        null=True, blank=True, default=None,
        related_name="app_user_driver",
    )
    total_distance = models.FloatField(
        null=True, blank=True, default=None,
    )
    suggested_donation = models.IntegerField(
        null=True, blank=True, default=None,
    )
    estimated_duration = models.FloatField(
        null=True, blank=True, default=None,
    )
    creation_timestamp = models.DateTimeField(
        auto_now=True,
    )

    """
    Ride Request Status
    """
    REQ_1 = "REQ_1"
    REQ_2 = "REQ_2"
    REQ_3 = "REQ_3"
    REQ_4 = "REQ_4"
    REQ_5 = "REQ_5"
    REQ_X = "REQ_X"
    STATUS = (
        (REQ_1, "REQ_1"),
        (REQ_2, "REQ_2"),
        (REQ_3, "REQ_3"),
        (REQ_4, "REQ_4"),
        (REQ_5, "REQ_5"),
        (REQ_X, "REQ_X"),
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        null=True, blank=True, default=None,
    )

    """
    Driver Status
    """
    RS_1_D = "RS_1_D"
    RS_2_D = "RS_2_D"
    RS_3_D = "RS_3_D"
    RS_8_D = "RS_8_D"
    RS_9_D = "RS_9_D"
    RS_10_D = "RS_10_D"
    DRIVER_STATUS = (
        (RS_1_D, "RS_1_D"),
        (RS_2_D, "RS_2_D"),
        (RS_3_D, "RS_3_D"),
        (RS_8_D, "RS_8_D"),
        (RS_9_D, "RS_9_D"),
        (RS_10_D, "RS_10_D"),
    )
    driver_status = models.CharField(
        max_length=32,
        choices=DRIVER_STATUS,
        null=True, blank=True, default=None,
    )

    """
    Passenger Status
    """
    RS_1_P = "RS_1_P"
    RS_4_P = "RS_4_P"
    RS_5_P = "RS_5_P"
    RS_7_P = "RS_7_P"
    RS_10_P = "RS_10_P"
    PASSENGER_STATUS = (
        (RS_1_P, "RS_1_P"),
        (RS_4_P, "RS_4_P"),
        (RS_5_P, "RS_5_P"),
        (RS_7_P, "RS_7_P"),
        (RS_10_P, "RS_10_P"),
    )
    passenger_status = models.CharField(
        max_length=32,
        choices=PASSENGER_STATUS,
        null=True, blank=True, default=None,
    )

    pickup_timestamp = models.DateTimeField(
        null=True, blank=True, default=None,
    )

    RED = "RED"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    GREEN = "GREEN"
    BLUE = "BLUE"
    COLOR_CODE = (
        (RED, "RED"),
        (YELLOW, "YELLOW"),
        (ORANGE, "ORANGE"),
        (GREEN, "GREEN"),
        (BLUE, "BLUE"),
    )
    color_code = models.CharField(
        max_length=32,
        choices=COLOR_CODE,
        null=True, blank=True, default=None,
    )

    number_code = models.IntegerField(
        null=True, blank=True, default=None,
    )

    # When we load the "set_location" page for a ride request, the user may
    # have other ride requests waiting to be assigned, completed, etc. If
    # the user want's to set up another ride, we should only pre-fetch the
    # request where "in_setup" is true; once the ride is past "PENDING_CONFIRM",
    # we should toggle this off. Every app user should only be able to have one
    # ride request that is "in_setup", therefore the unique together constraint.
    in_setup = models.BooleanField(
        null=True, blank=True, default=None,
    )

    @staticmethod
    def all():
        return RideRequest.objects.all()

    def passenger_upcoming_rides(app_user):
        return RideRequest.objects.filter(
            app_user=app_user,
            status__in=["REQ_2","REQ_3"],
        )

    def passenger_past_rides(app_user):
        return RideRequest.objects.filter(
            app_user=app_user,
            in_setup=None,
            status="REQ_5",
        )


    def passenger_cancel_ride_request(app_user, id):
        ride_request = RideRequest.objects.get(
            app_user=app_user,
            id=id,
        )
        if ride_request is None:
            raise Exception("No matching ride request found.")
        else:
            ride_request.status = "REQ_X"
            ride_request.save()


    def passenger_undo_cancel_ride_request(app_user, id):
        ride_request = RideRequest.objects.get(
            app_user=app_user,
            id=id,
        )
        if ride_request is None:
            raise Exception("No matching ride request found.")
        else:
            if ride_request.app_user_driver is None:
                ride_request.status = "REQ_2"
            else:
                ride_request.status = "REQ_3"
            ride_request.save()


    def driver_past_rides(app_user):
        return RideRequest.objects.filter(
            app_user_driver=app_user,
            status="REQ_5",
        )

    def driver_upcoming_rides(app_user):
        return RideRequest.objects.filter(
            app_user_driver=app_user,
            status="REQ_3",
        )

    def driver_availible_rides():
        return RideRequest.objects.filter(
            app_user_driver=None,
            status="REQ_2",
        ).order_by("-pickup_timestamp")

    def driver_claim_pickup(app_user, id):
        ride_request = RideRequest.objects.get(
            id=id,
        )
        if ride_request is None:
            raise Exception("No matching ride request found.")
        else:
            if ride_request.app_user_driver is not None:
                raise Exception("This ride has already been claimed by a driver.")
            else:
                ride_request.app_user_driver = app_user
                ride_request.status = "REQ_3"
                ride_request.color_code = ["RED", "YELLOW", "ORANGE", "GREEN", "BLUE", "ORANGE"][randrange(4)]
                ride_request.number_code = randrange(10, 99)
            ride_request.save()

    def driver_cancel_pickup(app_user, id):
        ride_request = RideRequest.objects.get(
            id=id,
        )
        if ride_request is None:
            raise Exception("No matching ride request found.")
        else:
            if ride_request.app_user_driver != app_user:
                raise Exception("You don't have permission to cancel this ride.")
            else:
                ride_request.app_user_driver = None
                ride_request.status = "REQ_2"
            ride_request.save()

    def driver_sidebar_info(app_user):
        return {
            "available_rides_count": len(RideRequest.driver_availible_rides()),
            "upcoming_rides_count": len(RideRequest.driver_upcoming_rides(app_user)),
            "past_rides_count": len(RideRequest.driver_past_rides(app_user)),
        }

    def rider_sidebar_info(app_user):
        return {
            "upcoming_rides_count": len(RideRequest.passenger_upcoming_rides(app_user)),
            "past_rides_count": len(RideRequest.passenger_past_rides(app_user)),
        }

    def ride_summary(self):
        return """
        <div class="alert alert-info">
            <p class="m-0">
                <strong>ID:</strong> {id}
            </p>
            <p class="m-0">
                <strong>Start:</strong> {start_address}
            </p>
            <p class="m-0">
                <strong>End:</strong> {end_address}
            </p>
            <p class="m-0">
                <strong>Timestamp:</strong> {pickup_timestamp}
            </p>
            <p class="m-0">
                <strong>Request Status:</strong> {status}
            </p>
            <p class="m-0">
                <strong>Passenger Status:</strong> {passenger_status}
            </p>
            <p class="m-0">
                <strong>Driver Status:</strong> {driver_status}
            </p>
            <p class="m-0">
                <strong>In Setup:</strong> {in_setup}
            </p>
            <a href="/ride_details/?id={id}">Details</a>
            <a href="/set_location" onclick="repeatRideRequest()"><span class="material-icons" style="float:right;">
                replay
            </span></a>
        </div>
        """.format(
            id=self.id,
            start_address=self.start_address,
            end_address=self.end_address,
            status=self.status,
            passenger_status=self.passenger_status,
            driver_status=self.driver_status,
            pickup_timestamp=self.pickup_timestamp,
            in_setup=self.in_setup,
        )

    def epoch(self):
        utc = self.pickup_timestamp.timestamp()
        print(utc)
        return utc

    """
    def __str__(self):
        return "%s (%s)" % (
            str(self.app_user.name),
            str(self.creation_timestamp),
        )
    """


class RideDonation(models.Model):
    ride_request = models.ForeignKey(
        RideRequest,
        on_delete=models.PROTECT,
        null=False, blank=False, default=None,
    )
    donation_id = models.CharField(
        max_length=500,
        null=False, blank=False, default=None,
    )
    checkout_session_id = models.CharField(
        max_length=500,
        null=False, blank=False, default=None,
    )
    amount = models.IntegerField(
        null=True, blank=True, default=None
    )
    currency = models.CharField(
        max_length=32,
        null=True, blank=True, default=None
    )
    success = models.BooleanField(
        null=True, blank=True, default=False
    )
    creation_timestamp = models.DateTimeField(
        auto_now=True)

    def initialize(self, checkout_session_id, ride_request_id, amount, currency):
        pass

    def print_summary(self):
        return """
        <h5 class="m-0 text-center">
            Your Donation:
        </h5>
        <p class="m-0 text-center">
            <strong>
                ${amount}
            </strong>
        </p>
        """.format(
            amount="%.2f" % (self.amount / 100),
        )

    def print_amount(self):
        return "$%.2f" % (self.amount / 100)


#-------------------------------------------------------------------------------
# OLD
#-------------------------------------------------------------------------------

class OldRideRequest(models.Model):
    class Meta:
        verbose_name= 'Current Ride Request'
        verbose_name_plural= 'Current Ride Requests'
    name = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    end_location = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    start_location = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    phone_number = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    pickup_time = models.TimeField(
        auto_now=False, auto_now_add=False, default=None)
    pickup_date = models.DateField(
        auto_now=False, auto_now_add=False, default=None)
    pronoun = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    special_req = models.TextField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    num_bags = models.IntegerField(
        null=False, blank=False, default=None)
    passenger_count = models.IntegerField(
        null=False, blank=False, default=None)
    driver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True, blank=True, default=None,
    )
    done = models.BooleanField(
        null=False, blank=False, default=False)
    creation_timestamp = models.DateTimeField(
        auto_now=True)


class OldDriverSignup(models.Model):
    class Meta:
        verbose_name= 'Driver Application'
        verbose_name_plural= 'Driver Applications'
    comments = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    first_name = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    last_name = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    contact_email = models.CharField(
        max_length=10, unique=False, null=True, blank=True, default=None)
    # phone_regex = RegexValidator(regex=r'^([1-9])+?1?\d{10,12}$', 
    #     message="Please enter a valid 10-12 digit phone number.")
    contact_phone = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
        # validators=[phone_regex],max_length=255, unique=False, null=True, blank=True, default=None)
    pronoun = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    smartphone_type = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    vehicle_doors = models.IntegerField(
        null=False, blank=False, default=None)
    vehicle_make = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    vehicle_model = models.CharField(
        max_length=255, unique=False, null=True, blank=True, default=None)
    vehicle_year = models.IntegerField(
        null=False, blank=False, default=None)
    yes_no_criminal_history = models.BooleanField(
        null=False, blank=False, default=False)
    yes_no_insurance = models.BooleanField(
        null=False, blank=False, default=False)
    yes_no_square = models.BooleanField(
        null=False, blank=False, default=False)
    creation_timestamp = models.DateTimeField(
        auto_now=True)
