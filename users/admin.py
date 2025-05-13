# Register your models here.
from django.contrib import admin
from orders.admin import OrderTabulareAdmin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", ]
    search_fields = ["username", "first_name", "last_name", "email", ]

    inlines = [OrderTabulareAdmin]