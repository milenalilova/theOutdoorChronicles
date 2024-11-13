from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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


#      TODO fix how the form displays in the template


class AppUserEditForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = '__all__'
