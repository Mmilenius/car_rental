from django import template
from users.models import Favorite

register = template.Library()


@register.simple_tag(takes_context=True)
def is_in_favorites(context, car_id):
    request = context['request']
    if not request.user.is_authenticated:
        return False

    return Favorite.objects.filter(user=request.user, car_id=car_id).exists()


@register.simple_tag(takes_context=True)
def favorites_count(context):
    request = context['request']
    if not request.user.is_authenticated:
        return 0
    return Favorite.objects.filter(user=request.user).count()