from django import forms
from SecuritySystem.account.models import AppUser,Profile

# class UserProfileForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#
#     class Meta:
#         model = AppUser
#         fields = ['username', 'email', 'password', 'first_name', 'last_name']  # Include the profile fields
#
#     def __init__(self, *args, **kwargs):
#         self.profile = kwargs.pop('profile')
#         super().__init__(*args, **kwargs)
#
#     def save(self, commit=True):
#         user = super().save(commit)
#         profile = self.profile
#         profile.first_name = self.cleaned_data.get('first_name')
#         profile.last_name = self.cleaned_data.get('last_name')
#         if commit:
#             user.save()
#             profile.save()
#         return user