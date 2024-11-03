from django import forms
from SecuritySystem.account.models import AppUser, Role


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name', 'id': 'floatingFirstName'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'floatingLastName'}))
    faculty_number = forms.CharField(max_length=9, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Faculty Numer', 'id': 'floatingFacultyNumber'}))
    chip = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'chip', 'id': 'floatingChip'}),
    )

    class Meta:
        model = AppUser
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'jhondoe', 'id': 'floatingText'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'name@example.com', 'id': 'floatingInput'}),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.profile.first_name
        self.fields['last_name'].initial = self.profile.last_name
        self.fields['faculty_number'].initial = self.profile.faculty_number
        self.fields['chip'].initial = self.profile.chip

    def save(self, commit=True):
        user = super().save()
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
            'role': forms.Select(
                attrs={'class': 'form-control', 'placeholder': 'role'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()
