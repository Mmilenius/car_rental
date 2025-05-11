from django.shortcuts import render, get_object_or_404

from cars.models import Cars  # не імпортуй модуль cars, бо це ім’я конфліктує

def catalog(request):
    all_cars = Cars.objects.all()
    context = {
        'title': 'Home - Каталог ',
        'cars': all_cars,
    }
    return render(request, 'cars/catalog.html', context)

def car(request, car_slug):
    car_obj = get_object_or_404(Cars, slug=car_slug)
    context = {
        'car': car_obj,
    }
    return render(request, 'cars/car.html', context)
