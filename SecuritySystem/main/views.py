from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic as views
import json

from django.views.decorators.csrf import csrf_exempt

from SecuritySystem.account.models import AppUser, Profile


# Create your views here.

class HomeView(views.TemplateView):
    template_name = 'main/home.html'

@method_decorator(csrf_exempt, name='dispatch')
class ChipCheckView(views.View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            faculty_number = data['user'].get('faculty_number')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON format or missing faculty number'}, status=400)


        try:
            profile = Profile.objects.get(faculty_number=faculty_number)
            user = AppUser.objects.get(username=profile.slug)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'No user with this faculty number found'}, status=404)


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
            faculty_number = data['user'].get('faculty_number') # zavisi kak shte davame jsona
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON format or missing faculty number'}, status=400)

        try:
            profile = Profile.objects.get(faculty_number=faculty_number)
            user = AppUser.objects.get(username=profile.slug)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'No user with this faculty number found'}, status=404)

        logout(request)
        return JsonResponse({'message': 'User logged out successfully.'})
        # else: ako shte checkvame dali e vlqzal predi tova
        #     return JsonResponse({'error': 'Invalid faculty_number or user not logged in.'}, status=400)
