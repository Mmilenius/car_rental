from django.shortcuts import render

from cars.models import Cars


def catalog(request):
    cars = Cars.objects.all()
    context = {
        'title': 'Home - Каталог ',
        'cars': cars,
    }



    return render(request, 'cars/catalog.html', context)

def car(request):
    return render(request, 'cars/car.html')