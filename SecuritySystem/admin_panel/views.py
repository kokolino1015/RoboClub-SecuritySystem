from django.contrib.auth.views import LoginView
from django.contrib.auth import  login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView

from SecuritySystem.account.forms import UserRegistrationFrom
from SecuritySystem.account.models import AppUser, Profile
from SecuritySystem.admin_panel.forms import UserProfileForm
from SecuritySystem.account.mixins import AdminRequiredMixin, AdminOrObserverRequiredMixin


class LogoutAndRedirectToSuperuserLoginView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('admin-login')

class AdminLoginView(LoginView):
    template_name = 'admin/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.role.id in [1, 2]:
            login(self.request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(self.request, 'Permission denied. You must be an Admin or Observer to log in.')
            return redirect('admin-login')


class AdminDashboardView(AdminOrObserverRequiredMixin, View):
    template_name = 'admin/dashboard.html'

    def get(self, request, *args, **kwargs):
        context = {
            'users': AppUser.objects.all(),
        }
        return render(request, self.template_name, context)

class UserCreateView(AdminRequiredMixin, CreateView):
    form_class = UserRegistrationFrom
    template_name = 'admin/user_creation_form.html'
    success_url = reverse_lazy('admin-dashboard')

class UserUpdateView(AdminRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'admin/edit_profile.html'
    success_url = reverse_lazy('admin-dashboard')
    slug_field = 'username'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        user = AppUser.objects.get(id=profile.user_id)
        return get_object_or_404(AppUser, username=user.username)

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        profile = Profile.objects.get(user=user)
        form = self.form_class(instance=user, profile=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        profile = Profile.objects.get(user=user)
        form = self.form_class(request.POST, instance=user, profile=profile)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = AppUser
    template_name = 'admin/delete_profile.html'
    success_url = reverse_lazy('admin-dashboard')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        user = AppUser.objects.get(id=profile.user_id)
        return get_object_or_404(AppUser, username=user.username)