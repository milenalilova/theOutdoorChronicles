from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from theOutdoorChronicles.accounts.models import Profile

UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
            }
        ),
        label='Username',
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email',
            }
        ),
        label='Email',
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
            }
        ),
        label='Password',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
            }
        ),
        label='Confirm Password',
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AppUserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = '__all__'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

# TODO get the field username to be able to change it.


class ProfileDeleteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Profile
        exclude = ('user',)
