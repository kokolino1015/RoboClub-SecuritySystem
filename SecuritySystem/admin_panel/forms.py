from django import forms
from SecuritySystem.account.models import AppUser, Role


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    faculty_number = forms.CharField(max_length=9, required=False)

    class Meta:
        model = AppUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        if self.profile:
            self.fields['first_name'].initial = self.profile.first_name
            self.fields['last_name'].initial = self.profile.last_name
            self.fields['faculty_number'].initial = self.profile.faculty_number

    def save(self, commit=True):
        user = super().save(commit)
        if self.profile:
            self.profile.first_name = self.cleaned_data.get('first_name')
            self.profile.last_name = self.cleaned_data.get('last_name')
            self.profile.faculty_number = self.cleaned_data.get('faculty_number')
            self.profile.slug = self.cleaned_data.get('username')
            if commit:
                user.save()
                self.profile.save()
        return user

class AssignRoleForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['role']
        widgets = {
            'role': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()