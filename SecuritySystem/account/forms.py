from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from SecuritySystem.account.models import Profile, AppUser

UserModel = get_user_model()


class UserRegistrationFrom(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        validators=(
            # validate_only_letters,
        )
    )
    last_name = forms.CharField(
        max_length=30,
        validators=(
            # validate_only_letters,
        )
    )
    faculty_number = forms.CharField(
        max_length=30,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def save(self, commit=True):
        user = super().save()
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            faculty_number=self.cleaned_data['faculty_number'],
            user=user,
            slug=user.username
        )
        if commit:
            profile.save()

        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'faculty_number')

    # You can add user fields here by overriding the __init__ method
    def __init__(self, *args, **kwargs):
        print(kwargs['instance'].user)
        user = AppUser.objects.filter(id=kwargs['instance'].user_id).first()
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'] = forms.CharField(initial=user.username)
            self.fields['email'] = forms.EmailField(initial=user.email)

    def save(self, commit=True):
        # Override save to also update the AppUser instance
        profile = super().save(commit=False)
        if commit:
            profile.save()
            user = profile.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.save()
        return profile