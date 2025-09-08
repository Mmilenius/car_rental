from django.contrib import admin
from django.urls import path, include

from carts import views

app_name = 'carts'

urlpatterns = [
    path('carts_add/', views.CartAddView.as_view(), name='carts_add'),
    path('carts_change/', views.CartChangeView.as_view(), name='carts_change'),
    path('carts_remove/', views.CartRemoveView.as_view(), name='carts_remove'),
]