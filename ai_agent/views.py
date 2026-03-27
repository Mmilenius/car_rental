import os
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cars.models import Cars

# НАЛАШТУВАННЯ API (Отримайте ключ тут: https://aistudio.google.com/app/apikey)
# Краще винести в .env або settings.py
GENAI_API_KEY = "AIzaSyBdF9lwYZg71njSjtOJQe5FsB_XWvXcECM"

genai.configure(api_key=GENAI_API_KEY)

# Налаштування моделі
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    def post(self, request):
        user_message = request.POST.get('message', '')
        image_file = request.FILES.get('image')

        # 1. Формуємо контекст (список авто з бази)
        cars = Cars.objects.all()
        inventory_context = "Ось список доступних автомобілів у нашому прокаті:\n"
        for car in cars:
            inventory_context += f"- {car.name} (Категорія: {car.category}, Ціна: ${car.price_for_sell}/день, ID: {car.id}, Slug: {car.slug})\n"

        # 2. Системна інструкція
        system_prompt = f"""
        Ти - віртуальний асистент сервісу оренди авто 'Car Rental'.
        Твоя мета: допомогти клієнту вибрати авто з НАШОГО автопарку.
        Спілкуйся українською мовою, будь ввічливим та лаконічним.

        {inventory_context}

        Якщо користувач скидає фото авто, спробуй знайти у нас максимально схоже (за класом, типом кузова, ціною).
        Якщо питають про ціни - бери їх з контексту вище.
        НЕ вигадуй авто, яких немає в списку.
        """

        try:
            chat_session = model.start_chat(history=[])

            parts = [system_prompt, f"Клієнт запитує: {user_message}"]

            # Якщо є фото, додаємо його до запиту
            if image_file:
                # Читаємо байти зображення
                image_data = {
                    'mime_type': image_file.content_type,
                    'data': image_file.read()
                }
                parts.append(image_data)
                parts.append("Клієнт надіслав фото авто. Знайди у нашому списку найбільш схоже авто або альтернативу.")

            # Відправляємо запит до Gemini
            response = model.generate_content(parts)
            ai_reply = response.text

            # Просте форматування Markdown в HTML (для жирного шрифту)
            import markdown
            ai_reply_html = markdown.markdown(ai_reply)

            return JsonResponse({'status': 'ok', 'answer': ai_reply_html})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error',
                                 'answer': 'Вибачте, зараз я відпочиваю. Спробуйте пізніше або зателефонуйте менеджеру.'})