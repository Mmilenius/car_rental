from django.http import JsonResponse
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from cars.models import Cars


class CartAddView(CartMixin, View):
    """
    View для додавання машини в кошик
    """

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

        response_data = {
            "message": "Машина додана в кошик",
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    """
    View для зміни періоду в кошику
    """

    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)

        cart.period = int(request.POST.get("period"))
        cart.save()

        period = cart.period

        response_data = {
            "message": "Період оновлено",
            "period": period,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    """
    View для видалення машини з кошика
    """

    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        period = cart.period
        cart.delete()

        response_data = {
            "message": "Машину видалено",
            "period_deleted": period,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)