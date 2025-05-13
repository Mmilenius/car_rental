from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
from cars.models import Cars
from carts.models import Cart
from carts.utils import get_user_carts


def carts_add(request):

    car_id = request.POST.get('car_id')
    car = Cars.objects.get(id=car_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, car=car)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.period += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, car=car, period=1)
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Машина добавленв в корзину",
        'cart_items_html': cart_items_html,
    }

    return JsonResponse(response_data)
def carts_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    period = cart.period
    cart.delete()

    user_cart = get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': user_cart}, request=request)

    response_data = {
        "message": "Машину видалено",
        "cart_items_html": cart_items_html,
        "period_deleted": period,
    }

    return JsonResponse(response_data)

def carts_change(request):
    ...