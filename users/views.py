from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistationForm, ProfileForm


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
                messages.success(request, f'{username}, Ви ввішли в аккаунт')

                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    contex = {
        'title': 'Home - Авторизація',
        'form': form,
    }
    return render(request, 'users/login.html', contex)

def registration(request):

    if request.method == 'POST':
        form = UserRegistationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'{user:username}, Ви успішно в аккаунт')
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistationForm()

    contex = {
        'title': 'Home - Реєстрація',
        'form': form,
    }
    return render(request, 'users/registration.html', contex)

@login_required
def profile(request):

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлений')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)

    contex = {
        'title': 'Home - Профіль',
        'form': form,
    }
    return render(request, 'users/profile.html', contex)


def users_cart(request):
    return render(request, 'users/users_cart.html')

@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, Ви вийшли з аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))

