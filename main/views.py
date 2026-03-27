from django.shortcuts import render
from django.http import HttpResponse

from cars.models import Cars
from cars.models import Categories
from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Головна'
        context['content'] = "Прокат автомобілі"
        context['categories'] = Categories.objects.all()
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Про сайт'
        context['content'] = "Про сайт"
        context['text_on_page'] = 'Текст на сторінці'
        return context


def index(request):
    # Отримуємо 3 останні додані авто (або можна відсортувати за популярністю)
    # [:3] означає "взяти перші 3"
    cars = Cars.objects.all().order_by('-id')[:3]

    context = {
        'title': 'Car Rental - Головна',
        'cars': cars,  # Передаємо автомобілі в шаблон
    }
    return render(request, 'main/index.html', context)