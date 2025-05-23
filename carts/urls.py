from django.contrib import admin
from django.urls import path, include

from carts import views

app_name = 'carts'

urlpatterns = [
    path('carts_add/', views.carts_add, name='carts_add'),
    path('carts_change/', views.carts_change, name='carts_change'),
    path('carts_remove/', views.carts_remove, name='carts_remove'),
]