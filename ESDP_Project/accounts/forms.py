from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from accounts.models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'surname', 'password1', 'password2',
            'phone'
        ]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())


