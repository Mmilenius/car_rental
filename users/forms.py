from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User

class UserLoginForm(AuthenticationForm):

    label = 'Ім’я користувача'
    username = forms.CharField(label = 'Ім’я користувача',
                               widget=forms.TextInput(attrs={"autofocus": True,
                                                             "class": "form-control",
                                                             'placeholder': 'Введіть Ваше ім`я'}))
    password = forms.CharField(label = 'Пароль',
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          "class": "form-control",
                                          'placeholder': 'Введіть Ваш пароль'}),
    )
    class Meta:
        model = User
        fields = ['email', 'password']