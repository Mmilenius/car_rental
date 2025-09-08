from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import transaction
from django.contrib import messages

from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm


class CreateOrderView(LoginRequiredMixin, View):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm

    def get(self, request):
        """Обробка GET запиту - відображення форми"""
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = self.form_class(initial=initial)

        context = {
            'title': 'Головна - Оформлення бронювання',
            'form': form,
            'order': True,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        """Обробка POST запиту - обробка форми"""
        form = self.form_class(data=request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Створити бронювання
                        order = self._create_order(user, form)

                        # Створити елементи замовлення
                        self._create_order_items(order, cart_items)

                        # Очистити кошик користувача після створення замовлення
                        cart_items.delete()

                        messages.success(request, 'Бронювання оформлено!')
                        return redirect('users:profile')

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('orders:create_order')

        # Якщо форма невалідна, повертаємо форму з помилками
        context = {
            'title': 'Головна - Оформлення бронювання',
            'form': form,
            'order': True,
        }
        return render(request, self.template_name, context=context)

    def _create_order(self, user, form):
        """Допоміжний метод для створення замовлення"""
        return Order.objects.create(
            user=user,
            phone_number=form.cleaned_data['phone_number'],
            end_date=form.cleaned_data['end_date'],
            start_date=form.cleaned_data['start_date'],
            requires_delivery=form.cleaned_data['requires_delivery'],
            delivery_address=form.cleaned_data['delivery_address'],
            payment_on_get=form.cleaned_data['payment_on_get'],
        )

    def _create_order_items(self, order, cart_items):
        """Допоміжний метод для створення елементів замовлення"""
        for cart_item in cart_items:
            car = cart_item.car
            name = cart_item.car.name
            price = cart_item.car.price_for_sell()
            period = cart_item.period

            OrderItem.objects.create(
                order=order,
                car=car,
                name=name,
                price=price,
                period=period,
            )