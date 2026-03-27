from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView

from cars.models import Cars, Categories
from cars.utilits import q_search


class CatalogView(ListView):
    model = Cars
    template_name = 'cars/catalog.html'
    context_object_name = 'cars'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        order_by = self.request.GET.get('order_by')
        on_sale = self.request.GET.get('on_sale')
        query = self.request.GET.get('q')

        if category_slug == 'all':
            cars = Cars.objects.all()
        elif query:
            cars = q_search(query)
        else:
            cars = Cars.objects.filter(category__slug=category_slug)
            if not cars.exists():
                raise Http404()

        if on_sale:
            cars = cars.filter(discount__gt=0)

        if order_by and order_by != 'default':
            cars = cars.order_by(order_by)

        return cars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Каталог'
        context['slug_url'] = self.kwargs.get('category_slug')
        context['categories'] = Categories.objects.all()
        return context


class CarView(DetailView):
    model = Cars
    template_name = 'cars/car.html'
    slug_url_kwarg = 'car_slug'
    context_object_name = 'car'

    def get_object(self, queryset=None):
        # Краще використовувати get_object_or_404, щоб викидало помилку 404, якщо авто не знайдено
        return get_object_or_404(Cars, slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name

        # --- Логіка "Схожих авто" ---
        current_car = self.object

        # 1. Шукаємо авто тієї ж категорії, виключаючи поточне, сортуємо випадково, беремо 4
        similar_cars = Cars.objects.filter(category=current_car.category).exclude(id=current_car.id).order_by('?')[:4]

        # 2. Якщо в категорії мало авто, беремо просто випадкові інші
        if not similar_cars:
            similar_cars = Cars.objects.exclude(id=current_car.id).order_by('?')[:4]

        context['similar_cars'] = similar_cars
        # -----------------------------

        return context