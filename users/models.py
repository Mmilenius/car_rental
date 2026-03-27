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