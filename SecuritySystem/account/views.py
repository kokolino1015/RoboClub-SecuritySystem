from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from SecuritySystem.account.forms import UserRegistrationFrom, EditProfileForm
from SecuritySystem.account.models import UserActivity, AppUser, Profile

UserModel = get_user_model()


class UserRegistrationView(views.CreateView):
    form_class = UserRegistrationFrom
    template_name = 'account/register_user.html'
    success_url = reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass

class ProfileDetailsView(views.DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'account/profile_details.html'
    context_object_name = 'profile'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.request.user.username
        return context

class EditProfileView(views.UpdateView, LoginRequiredMixin):
    form_class = EditProfileForm
    model = Profile
    template_name = 'account/edit_profile.html'
    slug_field = 'slug'

    def get_success_url(self):
        return reverse_lazy('profile detail', kwargs={'slug': self.request.user.username})


class DeleteProfileView(LoginRequiredMixin, views.DeleteView):
    model = UserModel
    fields = '__all__'
    template_name = 'account/delete_profile.html'
    slug_field = 'username'

    def get_success_url(self):
        return reverse_lazy('home')

