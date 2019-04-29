from accounts.models import Profile
from django.contrib import admin

from django.conf import settings

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ["user", "birthdate", "avatar"] if settings.AVATAR_SITE else ["user", "birthdate"]
    	