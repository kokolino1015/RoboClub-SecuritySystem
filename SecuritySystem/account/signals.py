from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivityLab, UserActivityWeb


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    try:
        login_method = request.session['login_method']
    except KeyError:
        pass
    if login_method == 'chip':
        UserActivityLab.objects.create(user=user, login_time=timezone.now())
    elif login_method == 'web':
        UserActivityWeb.objects.create(user=user, login_time=timezone.now())



@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        logout_method = request.session['logout_method']
    except KeyError:
        pass
    if logout_method == 'chip':
        activity = UserActivityLab.objects.filter(user=user).order_by('-id').first()
        activity.logout_time = timezone.now()
        activity.save()
    elif logout_method == 'web':
        activity = UserActivityWeb.objects.filter(user=user).order_by('-id').first()
        activity.logout_time = timezone.now()
        activity.save()
