from django.template.loader import render_to_string
from django.urls import reverse
from carts.models import Cart
from carts.utils import get_user_carts


class CartMixin:
    def get_cart(self, request, car=None, cart_id=None):
        """
        Отримує кошик користувача або по session_key
        """
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if car:
            query_kwargs["car"] = car
        if cart_id:
            query_kwargs["id"] = cart_id

        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        """
        Рендерить HTML кошика з урахуванням контексту
        """
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        # Якщо сторінка реферер - створення замовлення, додаємо ключ order: True
        referer = request.META.get('HTTP_REFERER')
        if referer and 'create_order' in referer:  # Адаптуйте під ваш URL
            context["order"] = True

        return render_to_string(
            "carts/includes/included_cart.html", context, request=request
        )