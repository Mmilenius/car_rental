from django.contrib import admin
from django.urls import path, include

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    # Оплата
    path('payment/<int:order_id>/', views.PaymentView.as_view(), name='payment_page'),
    path('payment/success/<int:order_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/confirm/', views.confirm_payment, name='confirm_payment'),

    # Webhook для Stripe
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]