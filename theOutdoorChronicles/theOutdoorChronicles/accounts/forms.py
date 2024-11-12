from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email')


class AppUserEditForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = '__all__'
