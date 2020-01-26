from django.db import models
from django.contrib.auth.models import User

import rowsheet.utils as rs_utils

class RideRequest(models.Model):
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


class Pronoun(models.Model):
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


class AppUser(models.Model):
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
    accommodations = models.ManyToManyField(Accommodation)
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
