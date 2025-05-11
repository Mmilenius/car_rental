from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404

from cars.models import Cars  # не імпортуй модуль cars, бо це ім’я конфліктує

def catalog(request, category_slug):

    order_by = request.GET.get('order_by', None)
    on_sale = request.GET.get('on_sale', None)
    page = request.GET.get('page', 1)

    if category_slug == 'all':
        all_cars = Cars.objects.all()
    else:
        all_cars = get_list_or_404(Cars.objects.filter(category__slug=category_slug))

    if on_sale:
        all_cars = Cars.objects.filter(discount__gt=0)

    if order_by and order_by != 'default':
        all_cars = Cars.objects.order_by(order_by)

    paginator = Paginator(all_cars, 4)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Home - Каталог ',
        'cars': current_page,
        'slug_url': category_slug,
    }
    return render(request, 'cars/catalog.html', context)

def car(request, car_slug):
    car_obj = get_object_or_404(Cars, slug=car_slug)
    context = {
        'car': car_obj,
    }
    return render(request, 'cars/car.html', context)
