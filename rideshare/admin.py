from django.contrib import admin

from .models import AppUser 
from .models import Pronoun 

class PronounAdmin(admin.ModelAdmin):
    fields = (
        "key",
        "display_name",
    )
    list_display = fields
    search_fields = fields
admin.site.register(Pronoun, PronounAdmin)

class AppUserAdmin(admin.ModelAdmin):
    fields = (
        "django_account",
        "username",
        "pronoun",
    ) 
    list_display = fields
    search_fields = fields
admin.site.register(AppUser, AppUserAdmin)
