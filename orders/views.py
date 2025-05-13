from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.db import transaction
from django.contrib import messages


from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm



@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Створити бронювання
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            end_date=form.cleaned_data['end_date'],
                            start_date=form.cleaned_data['start_date'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Створити форму аренди авто
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


                        # Очистити кошик користувача після створення замовлення
                        cart_items.delete()

                        messages.success(request, 'Замовлення оформлено!')
                        return redirect('users:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('orders:create_order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Головна - Оформлення бронювання',
        'form': form,
        'order': True,
    }
    return render(request, 'orders/create_order.html', context=context)

