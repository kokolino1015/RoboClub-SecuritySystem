from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from SecuritySystem.account.models import Profile

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
            user=user,
            slug=user.username
        )
        if commit:
            profile.save()

        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')