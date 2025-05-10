from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    context = {
        'title': 'Home - Головна',
        'content': 'Прокат автомобілів',
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Home - Про сайт',
        'content': 'Про сайт',
        'text_on_page': 'Текст на сторінці',
    }

    return render(request, 'main/about.html', context)