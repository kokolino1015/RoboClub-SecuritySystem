from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivity.objects.create(user=user, login_time=timezone.now())


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    activity = UserActivity.objects.filter(user=user).order_by('-id').first()
    activity.logout_time = timezone.now()
    activity.save()