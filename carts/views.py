from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from cars.models import Cars
from carts.utils import get_user_carts

class CartAddView(CartMixin, View):
    def post(self, request):
        car_id = request.POST.get("car_id")
        car = Cars.objects.get(id=car_id)
        cart = self.get_cart(request, car=car)

        if cart:
            cart.period += 1
            cart.save()
        else:
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                car=car,
                period=1
            )

        # Отримуємо оновлений кошик
        user_cart = get_user_carts(request)
        cart_items_html = self.render_cart(request)

        return JsonResponse({
            "message": "Машина додана в кошик",
            "cart_items_html": cart_items_html,
            # ВИПРАВЛЕНО: використовуємо total_period() замість total_quantity()
            "total_quantity": user_cart.total_period() if user_cart else 0,
        })

class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)

        # Зберігаємо період
        cart.period = int(request.POST.get("period"))
        cart.save()

        # Оновлюємо дані
        user_cart = get_user_carts(request)
        cart_items_html = self.render_cart(request)

        return JsonResponse({
            "message": "Період оновлено",
            "cart_items_html": cart_items_html,
            # ВИПРАВЛЕНО: використовуємо total_period()
            "total_quantity": user_cart.total_period() if user_cart else 0,
        })

class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        cart.delete()

        user_cart = get_user_carts(request)
        cart_items_html = self.render_cart(request)

        return JsonResponse({
            "message": "Машину видалено",
            "cart_items_html": cart_items_html,
            # ВИПРАВЛЕНО: використовуємо total_period()
            "total_quantity": user_cart.total_period() if user_cart else 0,
        })