from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView
from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistationForm, ProfileForm


class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        session_key = self.request.session.session_key

        if user:
            auth.login(self.request, user)
            messages.success(self.request, f'{username}, Ви ввійшли в аккаунт')

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            next_url = self.request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(reverse('main:index'))
        else:
            messages.error(self.request, 'Невірний логін або пароль')
            return self.form_invalid(form)


class UserRegistrationView(FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistationForm

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        session_key = self.request.session.session_key

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f'{user.username}, Ви успішно ввійшли в аккаунт')
        return redirect(reverse('main:index'))


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        orders = Order.objects.filter(user=request.user).prefetch_related(
            "orderitem_set__car"
        ).order_by("-id")

        context = {
            'title': 'Home - Профіль',
            'form': form,
            'orders': orders,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлений')
            return redirect(reverse('users:profile'))

        orders = Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("car"),
                )
            ).order_by("-id")

        context = {
            'title': 'Home - Профіль',
            'form': form,
            'orders': orders,
        }
        return render(request, self.template_name, context)


class UsersCartView(TemplateView):
    template_name = 'users/users_cart.html'


@method_decorator(login_required, name='dispatch')
class UserLogoutView(View):
    def get(self, request):
        messages.success(request, f'{request.user.username}, Ви вийшли з аккаунта')
        auth.logout(request)
        return redirect(reverse('main:index'))
