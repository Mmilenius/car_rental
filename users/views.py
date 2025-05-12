from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    contex = {
        'title': 'Home - Авторизація',
        'form': form,
    }
    return render(request, 'users/login.html', contex)

def registration(request):
    contex = {
        'title': 'Home - Реєстрація'
    }
    return render(request, 'users/registration.html', contex)

def profile(request):
    contex = {
        'title': 'Home - Профіль'
    }
    return render(request, 'users/profile.html', contex)

def logout(request):
    contex = {
        'title': 'Home - Вихід'
    }
    return render(request, '', contex)