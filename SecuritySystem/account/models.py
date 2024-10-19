from django.db import models

# Create your models here.
from django.contrib.auth import models as auth_models

from SecuritySystem.account.manager import AppUsersManager



class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    USERNAME_FIELD = 'email'
    objects = AppUsersManager()
    REQUIRED_FIELDS = ['username']


class Profile(models.Model):
    first_name = models.CharField(
        max_length=30,
    )
    last_name = models.CharField(
        max_length=30,

    )
    faculty_number = models.CharField(
        max_length=9,
    )
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    slug = models.SlugField()
