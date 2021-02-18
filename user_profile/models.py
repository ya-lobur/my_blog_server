from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class ProfileManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет учетную запись с переданными username, email и password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class Profile(AbstractBaseUser):
    """
    Учетная запись
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)
