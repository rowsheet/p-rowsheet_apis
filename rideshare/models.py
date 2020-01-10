from django.db import models
from django.contrib.auth.models import User

class Pronoun(models.Model):
    key = models.CharField(
        unique=True,
        max_length = 16,
        null = False, blank = False, default = None,
    )
    display_name = models.CharField(
        unique=True,
        max_length = 32,
        null = False, blank = False, default = None,
    )

class AppUser(models.Model):
    django_account = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        null = False, blank = False, default = None,
    )
    username = models.CharField(
        max_length = 64,
        null = False, blank = False, default = "Username Unset",
    )
    pronoun = models.ForeignKey(
        Pronoun,
        on_delete = models.PROTECT, # same as RESTRICT
        null = True , blank = True, default = None,
    )
