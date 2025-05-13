from django.db import models

from users.models import User
from cars.models import Cars

# Create your models here.

class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.car_price() for cart in self)

    def total_period(self):
        if self:
            return sum(cart.period for cart in self)
        return 0
class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Користувач')
    car = models.ForeignKey(to=Cars, on_delete=models.CASCADE, verbose_name='Машина')
    period = models.PositiveSmallIntegerField(default=0, verbose_name='Період')
    session_key = models.CharField(max_length=32, null=True,blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавлення машини')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    objects = CartQuerySet.as_manager()
    def cars_price(self):
        return round(self.car.price_for_sell() * self.period, 2)

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Машина {self.car.name} | Період {self.period}'