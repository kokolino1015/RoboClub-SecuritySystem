from django.urls import path
from .views import  AdminDashboardView, UserCreateView, \
    UserDeleteView, UserUpdateView, AssignRoleView

urlpatterns = [
    # path('logout-redirect', LogoutAndRedirectToSuperuserLoginView.as_view(), name='logout-redirect'),
    # path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('new-user-creation/', UserCreateView.as_view(), name='user-creation'),
    path('<slug:slug>/edit', UserUpdateView.as_view(), name='user-edit'),
    path('<slug:slug>/delete', UserDeleteView.as_view(), name='user-delete'),
    path('assign-role/<slug:slug>/', AssignRoleView.as_view(), name='assign_role'),

]