from django.shortcuts import render
from django.views import generic as views
# Create your views here.

class HomeView(views.TemplateView):
    template_name = 'home.html'