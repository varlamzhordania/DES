from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    is_online = models.BooleanField(default=False, help_text="User status", verbose_name='Online')

    def __str__(self):
        return self.username
