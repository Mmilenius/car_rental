from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.conf import settings
import stripe
import json

from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm

# Налаштування Stripe
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')


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

                        # Перевірити спосіб оплати
                        if form.cleaned_data['payment_on_get'] == '0':  # Оплата карткою
                            # Перенаправити на сторінку оплати
                            cart_items.delete()
                            return redirect('orders:payment_page', order_id=order.pk)
                        else:
                            # Оплата при отриманні - очистити кошик
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


class PaymentView(LoginRequiredMixin, View):
    """Сторінка оплати замовлення"""
    template_name = 'orders/payment.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # Перевірити, чи замовлення ще не оплачено
        if order.is_paid:
            messages.info(request, 'Це замовлення вже оплачено.')
            return redirect('users:profile')

        # Розрахувати загальну суму
        total_amount = self._calculate_total_amount(order)

        # Створити Stripe Payment Intent
        client_secret = self._create_payment_intent(order, total_amount, request)

        context = {
            'title': 'Оплата замовлення',
            'order': order,
            'total_amount': total_amount,
            'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
            'client_secret': client_secret,
        }
        return render(request, self.template_name, context)

    def _calculate_total_amount(self, order):
        """Розрахувати загальну суму замовлення"""
        order_items = OrderItem.objects.filter(order=order)
        total = sum(item.price * item.period for item in order_items)
        return total

    def _create_payment_intent(self, order, amount, request):
        """Створити Stripe Payment Intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe працює з копійками
                currency='uah',
                metadata={
                    'order_id': str(order.id),
                    'user_id': str(order.user.id)
                },
                automatic_payment_methods={'enabled': True},
            )
            return intent['client_secret']
        except stripe.error.StripeError as e:
            messages.error(request, f'Помилка створення платежу: {str(e)}')
            return None


class PaymentSuccessView(LoginRequiredMixin, View):
    """Сторінка успішної оплати"""
    template_name = 'orders/payment_success.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # Розрахувати загальну суму
        total_amount = self._calculate_total_amount(order)

        context = {
            'title': 'Оплата успішна',
            'order': order,
            'total_amount': total_amount,
        }
        return render(request, self.template_name, context)

    def _calculate_total_amount(self, order):
        """Розрахувати загальну суму замовлення"""
        order_items = OrderItem.objects.filter(order=order)
        total = sum(item.price * item.period for item in order_items)
        return total


@csrf_exempt
def stripe_webhook(request):
    """Webhook для обробки подій від Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']

        try:
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.status = 'Оплачено'
            order.save()

            # Очистити кошик користувача після успішної оплати
            Cart.objects.filter(user=order.user).delete()

        except Order.DoesNotExist:
            pass

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']

        try:
            order = Order.objects.get(id=order_id)
            order.status = 'Помилка оплати'
            order.save()
        except Order.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'})


@require_POST
def confirm_payment(request):
    """AJAX endpoint для підтвердження оплати"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        payment_intent_id = data.get('payment_intent_id')
        simulated = data.get('simulated', False)

        order = get_object_or_404(Order, id=order_id, user=request.user)

        if simulated:
            # Симульована оплата через Google Pay
            order.is_paid = True
            order.status = 'Оплачено'
            order.save()

            # Очистити кошик
            Cart.objects.filter(user=request.user).delete()

            return JsonResponse({
                'success': True,
                'redirect_url': f'/orders/payment/success/{order.id}/'
            })
        else:
            # Звичайна оплата через картку
            # Перевірити статус платежу в Stripe
            try:
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

                if payment_intent['status'] == 'succeeded':
                    order.is_paid = True
                    order.status = 'Оплачено'
                    order.save()

                    # Очистити кошик
                    Cart.objects.filter(user=request.user).delete()

                    return JsonResponse({
                        'success': True,
                        'redirect_url': f'/orders/payment/success/{order.id}/'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Платіж не підтверджено'
                    })

            except stripe.error.StripeError as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })