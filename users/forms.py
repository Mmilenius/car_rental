from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User

class UserLoginForm(AuthenticationForm):

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

class UserRegistationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

class ProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
        )

    iamge = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()