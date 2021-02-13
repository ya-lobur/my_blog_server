from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True)
