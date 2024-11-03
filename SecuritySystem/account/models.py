from django.db import models

# Create your models here.
from django.contrib.auth import models as auth_models

from SecuritySystem.account.manager import AppUsersManager


class Role(models.Model):
    name = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.name


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        max_length=30,
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
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL, null=True
    )

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = Role.objects.get(name='normal_user')
        super().save(*args, **kwargs)


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
    chip = models.CharField(unique=True, max_length=255)
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    slug = models.SlugField()


class UserActivityLab(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE
    )
    login_time = models.DateTimeField(
        null=True,
        blank=True
    )
    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - Last login: {self.login_time}, Last logout: {self.logout_time}"

class UserActivityWeb(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE
    )
    login_time = models.DateTimeField(
        null=True,
        blank=True
    )
    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - Last login: {self.login_time}, Last logout: {self.logout_time}"
