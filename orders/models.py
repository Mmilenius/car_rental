from django.db import models

# Create your models here.
from cars.models import Cars

from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.cars_price() for cart in self)

    def total_period(self):
        if self:
            return sum(cart.period for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Користувач",
                             default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення бронювання")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата початку оренди")
    end_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата зікінченян оренди")
    requires_delivery = models.BooleanField(default=False, verbose_name="Потрібна доставка")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адреса доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при отриманні")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='Опрацьовується', verbose_name="Статус замовлення")

    class Meta:
        db_table = "order"
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"
        ordering = ("id",)

    def __str__(self):
        return f"Замовлдення № {self.pk} | Клієнт {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Замовлення")
    car = models.ForeignKey(to=Cars, on_delete=models.SET_DEFAULT, null=True, verbose_name="Машина",
                                default=None)
    name = models.CharField(max_length=150, verbose_name="Назва")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Ціна")
    period = models.PositiveIntegerField(default=0, verbose_name="Термін")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення бронювання")

    class Meta:
        db_table = "order_item"
        verbose_name = "Орендовану машину"
        verbose_name_plural = "Орендовані машини"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def cars_price(self):
        return round(self.cars.price_for_sell() * self.period, 2)

    def __str__(self):
        return f"Машина {self.name} | Замовлення № {self.order.pk}"