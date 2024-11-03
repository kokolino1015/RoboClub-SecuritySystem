from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from SecuritySystem.main.views import HomeView,  ChipLogoutView, ChipCheckView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('check-chip/', ChipCheckView.as_view(), name='check-card'),
    path('logout-chip/', ChipLogoutView.as_view(), name='logout-card'),
]