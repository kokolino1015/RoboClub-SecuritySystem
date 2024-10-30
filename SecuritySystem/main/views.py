from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic as views
import json

from SecuritySystem.account.models import AppUser, Profile


# Create your views here.

class HomeView(views.TemplateView):
    template_name = 'main/home.html'


class CardCheckView(views):
    def post(self, request, *args, **kwargs):
        # Step 1: Parse JSON data
        try:
            data = json.loads(request.body)
            faculty_number = data.get('faculty_number')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON format or missing faculty_number'}, status=400)

        # Step 2: Check if a user exists with this card ID
        try:
            profile = Profile.objects.get(faculty_number=faculty_number)
            user = AppUser.objects.get(username=profile.slug)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'No user with this faculty number found'}, status=404)

        # Step 3: Log the user in
        login(request, user)

        # Step 4: Return a success response
        return JsonResponse({
            'message': 'User logged in successfully',
            'user': {
                'username': user.username,
                'email': user.email,
            }
        })

class CardLogoutView(views):
    def post(self, request, *args, **kwargs):
        # Step 1: Parse JSON data for card_id
        try:
            data = json.loads(request.body)
            faculty_number = data.get('faculty_number')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON format or missing faculty_number'}, status=400)

        # Step 2: Check if the user is authenticated and card_id matches
        if request.user.is_authenticated and request.user.faculty_number == faculty_number:
            # Step 3: Log out the user
            logout(request)
            # Step 4: Return a success response
            return JsonResponse({'message': 'User logged out successfully.'})
        else:
            # Step 5: Return an error response if card_id does not match
            return JsonResponse({'error': 'Invalid faculty_number or user not logged in.'}, status=400)
