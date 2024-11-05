from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from SecuritySystem.account.views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileDetailsView, \
    EditProfileView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='home'), name='logout'),
    path('<slug:slug>/', ProfileDetailsView.as_view(), name='details'),
    path('<slug:slug>/edit', EditProfileView.as_view(), name='edit profile'),
    # path('<slug:slug>/delete', DeleteProfileView.as_view(), name='delete profile'),
]