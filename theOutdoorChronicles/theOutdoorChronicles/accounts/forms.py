from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', )

#      TODO fix how the form displays in the template


class AppUserEditForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = '__all__'
