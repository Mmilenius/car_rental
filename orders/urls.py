from django.contrib import admin
from django.urls import path, include

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
]