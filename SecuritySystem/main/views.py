from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic as views
import json

from django.views.decorators.csrf import csrf_exempt

from SecuritySystem.account.models import AppUser, Profile, UserActivityLab


class HomeView(views.TemplateView):
    template_name = 'main/home.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role.id == 1 or request.user.role.id == 2:
                return redirect('admin-dashboard')
            else:
                return redirect('details', request.user.username)
        return redirect('login')

@method_decorator(csrf_exempt, name='dispatch')
class ChipCheckView(views.View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            chip = data['user'].get('chip')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON format or missing chip'}, status=400)


        try:
            profile = Profile.objects.get(chip=chip)
            user = AppUser.objects.get(username=profile.slug)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'No user with this chip found'}, status=404)

        activity = UserActivityLab.objects.filter(user=user).order_by('-id').first()
        logout_time = activity.logout_time
        if not logout_time:
            return JsonResponse({
            'message': 'User is already logged in, can\'t go in again with this card',
            'user': {
                'username': user.username,
                'email': user.email,
            }
        })
        request.session['login_method'] = 'chip'
        login(request, user)


        return JsonResponse({
            'message': 'User logged in successfully',
            'user': {
                'username': user.username,
                'email': user.email,
            }
        })

@method_decorator(csrf_exempt, name='dispatch')
class ChipLogoutView(views.View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            chip = data['user'].get('chip') # zavisi kak shte davame jsona
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON format or missing chip'}, status=400)

        try:
            profile = Profile.objects.get(chip=chip)
            user = AppUser.objects.get(username=profile.slug)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'No user with this chip found'}, status=404)
        activity = UserActivityLab.objects.filter(user=user).order_by('-id').first()
        logout_time = activity.logout_time
        if logout_time:
            return JsonResponse({'message': 'User already is logged out.'})
        request.session['logout_method'] = 'chip'
        logout(request)
        return JsonResponse({'message': 'User logged out successfully.'})
