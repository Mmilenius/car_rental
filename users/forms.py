from django import forms
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import LoginForm, SignupForm
from users.models import User


class UserLoginForm(LoginForm):
    login = forms.CharField(
        label="Email або Username",  # Додайте явно label тут
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть Email або Username',
            'class': 'form-control',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введіть Ваш пароль',
            'class': 'form-control'
        })
    )

    # Додайте цей метод, щоб переконатися, що label застосовується
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Email або Username"


class UserRegistationForm(SignupForm):

    field_order = [
        'first_name',
        'last_name',
        'username',
        'email',
        'password1',
        'password2'
    ]

    first_name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={
            'placeholder': "Введіть ваше ім'я",
            'class': 'form-control',
            'autofocus': True
        })
    )
    last_name = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={
            'placeholder': "Введіть ваше прізвище",
            'class': 'form-control'
        })
    )
    username = forms.CharField(
        label="Ім'я користувача",
        widget=forms.TextInput(attrs={
            'placeholder': "Введіть ім'я користувача",
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': "Введіть ваш email",
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': "Введіть пароль",
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={
            'placeholder': "Підтвердіть пароль",
            'class': 'form-control'
        })
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

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