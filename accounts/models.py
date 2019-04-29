from django.contrib.auth.models import User
from django.db import models

from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    if settings.AVATAR_SITE:
    	avatar = models.ImageField(upload_to="user_avatars/%Y/%m/%d", blank=True)

    def __str__(self):
        return "Профиль пользователя %s" % self.user.username