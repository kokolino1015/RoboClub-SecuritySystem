from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role.id == 1

    def handle_no_permission(self):
        # raise PermissionDenied("You must be an Admin to access this page.")
        return render(self.request, 'admin/permission_denied.html', status=403)


class ObserverRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role.id == 2

    def handle_no_permission(self):
        return render(self.request, 'admin/permission_denied.html', status=403)
        # raise PermissionDenied("You must be an Observer to access this page.")


class AdminOrObserverRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.role.id == 2 or self.request.user.role.id == 1)

    def handle_no_permission(self):
        # raise PermissionDenied("You must be a Admin or Observer to access this page.")
        return render(self.request, 'admin/permission_denied.html', status=403)

