# Register your models here.
from django.contrib import admin
from users.models import User, FineNotification, IncidentReport
from orders.admin import OrderTabulareAdmin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", ]
    search_fields = ["username", "first_name", "last_name", "email", ]

    inlines = [OrderTabulareAdmin]

@admin.register(FineNotification)
class FineNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'amount', 'is_paid', 'issued_date')
    list_filter = ('is_paid', 'issued_date')
    search_fields = ('user__username', 'car__name')

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'incident_type', 'status', 'created_timestamp')
    list_filter = ('status', 'incident_type')
    search_fields = ('user__username', 'description')