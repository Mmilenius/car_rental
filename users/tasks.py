from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User, Newsletter
@shared_task
def send_newsletter_task(newsletter_id):
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)

        # ПЕРЕВІРКА ПРАПОРЦЯ
        if newsletter.use_target_emails and newsletter.target_emails:
            # Режим 1: Тільки вказані адреси
            raw_emails = newsletter.target_emails.split(',')
            recipient_list = [email.strip() for email in raw_emails if email.strip()]
        else:
            # Режим 2: Стандартна ситуація (всі підписники)
            subscribers = User.objects.filter(is_subscribed=True).exclude(email='')
            recipient_list = list(subscribers.values_list('email', flat=True))

        if not recipient_list:
            return "Отримувачів не знайдено. Відправку скасовано."

        # Фізична відправка через SMTP
        send_mail(
            subject=newsletter.subject,
            message=newsletter.content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        # Фіксація результату
        newsletter.is_sent = True
        newsletter.sent_at = timezone.now()
        newsletter.save()

        return f"Розсилка '{newsletter.subject}' успішно відправлена на {len(recipient_list)} адрес."

    except Newsletter.DoesNotExist:
        return "Помилка: Розсилку з таким ID не знайдено."