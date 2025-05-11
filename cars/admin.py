from django.contrib import admin

# Register your models here.
from cars.models import Categories, Cars

#admin.site.register(Categories)
#admin.site.register(Cars)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}