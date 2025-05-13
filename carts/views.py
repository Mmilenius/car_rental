from django.shortcuts import render, redirect

# Create your views here.
from cars.models import Cars
from carts.models import Cart
def carts_add(request, car_slug):
    car = Cars.objects.get(slug=car_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, car=car)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.period += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, car=car, period=1)

    return redirect(request.META['HTTP_REFERER'])
def carts_remove(request):
    ...
def carts_change(request):
    ...