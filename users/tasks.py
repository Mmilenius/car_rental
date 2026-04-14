from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from .models import User, Newsletter


@shared_task
def send_newsletter_task(newsletter_id):
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)

        # ПЕРЕВІРКА ПРАПОРЦЯ (Ваша існуюча логіка)
        if newsletter.use_target_emails and newsletter.target_emails:
            raw_emails = newsletter.target_emails.split(',')
            recipient_list = [email.strip() for email in raw_emails if email.strip()]
        else:
            subscribers = User.objects.filter(is_subscribed=True).exclude(email='')
            recipient_list = list(subscribers.values_list('email', flat=True))

        if not recipient_list:
            return "Отримувачів не знайдено. Відправку скасовано."

        # ПІДГОТОВКА ДАНИХ ДЛЯ ШАБЛОНУ
        # Базовий URL вашого сайту (в реальному проекті краще брати з налаштувань або Site framework)
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

        # Формуємо повне посилання на картинку, якщо вона є
        image_url = None
        if newsletter.image:
            image_url = f"{site_url}{newsletter.image.url}"

        context = {
            'subject': newsletter.subject,
            'content': newsletter.content,
            'image_url': image_url,
            'site_url': site_url,
        }

        # ГЕНЕРАЦІЯ HTML ТА ТЕКСТОВОЇ ВЕРСІЇ
        html_message = render_to_string('emails/newsletter_email.html', context)
        # Звичайна текстова версія потрібна для поштових клієнтів, які не підтримують HTML (або для спам-фільтрів)
        plain_message = strip_tags(html_message)

        # ФІЗИЧНА ВІДПРАВКА ЧЕРЕЗ SMTP
        msg = EmailMultiAlternatives(
            subject=newsletter.subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[],  # Ховаємо список отримувачів один від одного (для масової розсилки)
            bcc=recipient_list,  # Всі адреси йдуть у приховану копію (BCC)
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)

        # Фіксація результату
        newsletter.is_sent = True
        newsletter.sent_at = timezone.now()
        newsletter.save()

        return f"Розсилка '{newsletter.subject}' (HTML) успішно відправлена на {len(recipient_list)} адрес."

    except Newsletter.DoesNotExist:
        return "Помилка: Розсилку з таким ID не знайдено."