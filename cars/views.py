from django.shortcuts import render

def catalog(request):
    return render(request, 'cars/catalog.html')

def car(request):
    return render(request, 'cars/car.html')