from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from SecuritySystem.main.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]