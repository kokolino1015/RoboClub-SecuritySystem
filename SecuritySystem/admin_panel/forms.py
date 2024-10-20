from django import forms
from SecuritySystem.account.models import AppUser


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        if self.profile:
            self.fields['first_name'].initial = self.profile.first_name
            self.fields['last_name'].initial = self.profile.last_name

    def save(self, commit=True):
        user = super().save(commit)
        if self.profile:
            self.profile.first_name = self.cleaned_data.get('first_name')
            self.profile.last_name = self.cleaned_data.get('last_name')
            self.profile.slug = self.cleaned_data.get('username')
            if commit:
                user.save()
                self.profile.save()
        return user
