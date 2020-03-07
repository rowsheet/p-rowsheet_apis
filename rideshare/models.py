import enum

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

import rowsheet.utils as rs_utils


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
    def get_accommodations(self):
        return ",".join([str(acc) for acc in self.accommodations.all()])


class RideRequest(models.Model):
    class Meta:
        verbose_name= 'Rider Request (development)'
        verbose_name_plural= 'Rider Requests (development)'
    start_name = models.CharField(
        unique=True,
        max_length=64,
        null=False, blank=False, default=None,
    )
    start_address = models.CharField(
        unique=True,
        max_length=128,
        null=False, blank=False, default=None,
    )
    start_place_id = models.CharField(
        unique=True,
        max_length=256,
        null=False, blank=False, default=None,
    )
    end_name = models.CharField(
        unique=True,
        max_length=64,
        null=False, blank=False, default=None,
    )
    end_address = models.CharField(
        unique=True,
        max_length=128,
        null=False, blank=False, default=None,
    )
    end_place_id = models.CharField(
        unique=True,
        max_length=256,
        null=False, blank=False, default=None,
    )
    ride_utc = models.IntegerField(
        null=False, blank=False, default=None,
    )
    csrf_token = models.CharField(
        unique=True,
        max_length=256,
        null=False, blank=False, default=None,
    )
    app_user = models.ForeignKey(
        AppUser,
        on_delete=models.PROTECT,
        null=False, blank=False, default=None,
        unique=True,
    )
    creation_timestamp = models.DateTimeField(
        auto_now=True,
    )
    PENDING_CONFIRM = "PENDING_CONFIRM"
    PENDING_DRIVER = "PENDING_DRIVER"
    PENDING_PICKUP = "PENDING_PICKUP"
    PENDING_DROPOFF = "PENDING_DROPOFF"
    CANCELED = "CANCELED"
    DONE = "DONE" # Note: Consider NULL => DONE
    STATUS = (
        (PENDING_CONFIRM, "PENDING_CONFIRM"),
        (PENDING_DRIVER, "PENDING_DRIVER"),
        (PENDING_PICKUP, "PENDING_PICKUP"),
        (PENDING_DROPOFF, "PENDING_DROPOFF"),
        (CANCELED, "CANCELED"),
        (DONE, "DONE"), # Note: Consider NULL => DONE
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        null=True, blank=True, default=None,
    )


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
