from django.db import models
from django.contrib.auth.models import AbstractUser
from cars.models import Cars

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        db_table = 'user'
        verbose_name = 'Користувача'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.username

class Favorite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Користувач')
    car = models.ForeignKey(to=Cars, on_delete=models.CASCADE, verbose_name='Автомобіль')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')

    class Meta:
        db_table = 'favorite'
        verbose_name = 'Обране'
        verbose_name_plural = 'Обрані'
        # Унікальна пара, щоб не можна було додати одне авто двічі
        unique_together = ('user', 'car')

    def __str__(self):
        return f"Обране {self.user.username} | {self.car.name}"

class IncidentReport(models.Model):
    INCIDENT_TYPES = [
        ('damage', 'Пошкодження авто'),
        ('dtp', 'ДТП (Аварія)'),
        ('breakdown', 'Технічна поломка'),
        ('other', 'Інше'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Очікує розгляду'),
        ('processing', 'В процесі'),
        ('resolved', 'Вирішено'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Користувач')
    order = models.ForeignKey(to='orders.Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пов\'язане замовлення')
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES, verbose_name='Тип події')
    description = models.TextField(verbose_name='Опис проблеми')
    photo = models.ImageField(upload_to='incident_photos/', blank=True, null=True, verbose_name='Фото доказ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        db_table = 'incident_report'
        verbose_name = 'Звіт про інцидент'
        verbose_name_plural = 'Звіти про інциденти'

class FineNotification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Користувач')
    car = models.ForeignKey(to=Cars, on_delete=models.CASCADE, verbose_name='Автомобіль')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сума штрафу')
    reason = models.TextField(verbose_name='Причина штрафу (стаття/опис)')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    issued_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата виписки штрафу')

    class Meta:
        db_table = 'fine_notification'
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафи'