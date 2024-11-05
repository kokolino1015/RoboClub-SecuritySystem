from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from SecuritySystem.account.models import Profile, AppUser

UserModel = get_user_model()


class UserRegistrationFrom(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'id': 'floatingFirstName'}),
        validators=(
            # validate_only_letters,
        )
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'floatingLastName'}),
        validators=(
            # validate_only_letters,
        )
    )
    faculty_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Faculty Numer', 'id': 'floatingFacultyNumber'}),
    )
    chip = forms.CharField(
        widget=forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'chip', 'id': 'floatingChip'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].widgets = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'floatingPassword'})
        self.fields['password2'].widgets = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'id': 'floatingPassword2'})

    class Meta:
        model = UserModel
        fields = ('email', 'username')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'jhondoe', 'id': 'floatingText'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'name@example.com', 'id': 'floatingInput'}),
        }

    def save(self, commit=True):
        user = super().save()
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            faculty_number=self.cleaned_data['faculty_number'],
            user=user,
            slug=user.username,
            chip=self.cleaned_data['chip'],
        )
        if commit:
            profile.save()

        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'faculty_number')
        widgets ={
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'jhondoe', 'id': 'floatingText'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'name@example.com', 'id': 'floatingInput'}),
            'faculty_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Faculty Numer', 'id': 'floatingFacultyNumber'}
            ),
            # 'chip': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': 'chip', 'id': 'floatingChip'}
            # )
        }

    # You can add user fields here by overriding the __init__ method
    def __init__(self, *args, **kwargs):
        user = AppUser.objects.filter(id=kwargs['instance'].user_id).first()
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'] = forms.CharField(
                initial=user.username,
                widget = forms.TextInput(
                    attrs = {'class': 'form-control', 'placeholder': 'jhondoe', 'id': 'floatingText'}
                )
            )
            self.fields['email'] = forms.EmailField(
                initial=user.email,
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'name@example.com',
                    'id': 'floatingInput'
                })
            )

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            user = profile.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.save()
        return profile