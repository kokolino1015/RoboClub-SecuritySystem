from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic as views
import json

from django.views.decorators.csrf import csrf_exempt

from SecuritySystem.account.models import AppUser, Profile


class HomeView(views.TemplateView):
    template_name = 'main/home.html'

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
        request.session['logout_method'] = 'chip'
        logout(request)
        return JsonResponse({'message': 'User logged out successfully.'})
