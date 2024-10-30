from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from SecuritySystem.main.views import HomeView, CardCheckView, CardLogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('check-card/', CardCheckView.as_view(), name='check-card'),
    path('logout-card/', CardLogoutView.as_view(), name='logout-card'),
]