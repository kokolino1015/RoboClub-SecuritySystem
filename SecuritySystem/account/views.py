from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login, get_user_model, logout
from django.urls import reverse_lazy
from django.views import generic as views
from SecuritySystem.account.forms import UserRegistrationFrom, EditProfileForm
from SecuritySystem.account.models import AppUser, Profile, UserActivityWeb  # UserActivity

UserModel = get_user_model()


class UserRegistrationView(views.CreateView):
    form_class = UserRegistrationFrom
    template_name = 'account/register_user.html'
    success_url = reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        self.request.session['logout_method'] = 'web'
        login(self.request, self.object)
        return result


class UserLoginView(LoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        self.request.session['login_method'] = 'web'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        request.session['logout_method'] = 'web'
        response = super().dispatch(request, *args, **kwargs)
        return response

class ProfileDetailsView(LoginRequiredMixin,views.DetailView):
    model = AppUser
    template_name = 'account/profile_details.html'
    context_object_name = 'profile'
    slug_field = 'slug'

    def get_queryset(self):
        return Profile.objects.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.request.user.username
        context['update_permission'] = False
        if self.request.user.role.id == 1 or self.request.user.id == self.object.user.id:
            context['update_permission'] = True
        context['activity'] = UserActivityWeb.objects.filter(user_id=self.object.user_id).all()
        return context

class EditProfileView(LoginRequiredMixin, views.UpdateView):
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

