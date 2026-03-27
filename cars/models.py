from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Cars(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Механічна'),
        ('automatic', 'Автомат'),
        ('semi_auto', 'Робот'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('hybrid', 'Гібрид'),
        ('electric', 'Електро'),
    ]

    name = models.CharField(max_length=150, unique=True, verbose_name='Машина')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Опис')
    image = models.ImageField(upload_to='cars_image', blank=True, null=True, verbose_name='Зображення')

    # Ціни
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Ціна за добу')
    discount = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Знижка %')

    # Технічні характеристики
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Об\'єм двигуна (л)', null=True,
                                        blank=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, verbose_name='Тип палива', default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, verbose_name='Коробка передач',
                                    default='manual')
    fuel_consumption = models.CharField(max_length=50, verbose_name='Витрата палива', blank=True,
                                        null=True)  # наприклад "6-8л/100км"
    doors = models.IntegerField(verbose_name='Кількість дверей', default=4)
    seats = models.IntegerField(verbose_name='Кількість місць', default=5)
    has_air_conditioning = models.BooleanField(default=True, verbose_name='Кондиціонер')

    # Умови оренди
    min_age = models.IntegerField(default=25, verbose_name='Мінімальний вік водія')
    min_experience = models.IntegerField(default=1, verbose_name='Мінімальний стаж водіння (років)')
    deposit = models.DecimalField(max_digits=7, decimal_places=2, default=300.00, verbose_name='Депозит $')

    category = models.ForeignKey(to=Categories, on_delete=models.PROTECT, verbose_name='Категорія')

    class Meta:
        db_table = 'car'
        verbose_name = 'Машину'
        verbose_name_plural = 'Машини'
        ordering = ('id',)

    def __str__(self):
        return self.name

    def displey_id(self):
        return f'{self.id:04}'

    def price_for_sell(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

    def total_price(self, period):
        return round(self.price_for_sell() * period, 2)

    def get_transmission_display_ua(self):
        """Повертає переклад коробки передач українською"""
        transmission_dict = {
            'manual': 'механічна',
            'automatic': 'автомат',
            'semi_auto': 'робот',
        }
        return transmission_dict.get(self.transmission, self.transmission)

    def get_fuel_type_display_ua(self):
        """Повертає переклад типу палива українською"""
        fuel_dict = {
            'petrol': 'бензин',
            'diesel': 'дизель',
            'hybrid': 'гібрид',
            'electric': 'електро',
        }
        return fuel_dict.get(self.fuel_type, self.fuel_type)