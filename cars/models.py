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
    name = models.CharField(max_length=150, unique=True, verbose_name='Машина')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Опис')
    image = models.ImageField(upload_to='cars_image', blank=True, null=True, verbose_name='Зображення')
    price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Ціна')
    discount = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Знижка')
    category = models.ForeignKey(to=Categories, on_delete=models.PROTECT, verbose_name='Категорія')

    class Meta:
        db_table = 'car'
        verbose_name = 'Машину'
        verbose_name_plural = 'Машини'

    def __str__(self):
        return self.name