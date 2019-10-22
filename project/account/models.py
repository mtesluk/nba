from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    START_MONEY = 100

    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=30, blank=True)
    credits = models.FloatField(default=START_MONEY)

    def __str__(self):
        return self.user.username
