# Register your models here.
from django.contrib import admin
from users.models import User, FineNotification, IncidentReport
from orders.admin import OrderTabulareAdmin
from django.utils import timezone
from .models import User, Newsletter
# from .tasks import send_newsletter_task

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


@admin.action(description='Відправити вибрані розсилки підписникам')
def send_newsletters(modeladmin, request, queryset):
    # queryset - це список тих розсилок, які адмін виділив галочками
    for newsletter in queryset:
        if not newsletter.is_sent:
            # ТУТ БУДЕ ЗАПУСК CELERY ЗАДАЧІ:
            # send_newsletter_task.delay(newsletter.id)

            # Поки що просто робимо вигляд, що відправили (для тесту)
            newsletter.is_sent = True
            newsletter.sent_at = timezone.now()
            newsletter.save()

    modeladmin.message_user(request, f"Розсилку успішно додано в чергу на відправку!")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'is_sent', 'sent_at')
    list_filter = ('is_sent',)
    search_fields = ('subject', 'content')
    actions = [send_newsletters]