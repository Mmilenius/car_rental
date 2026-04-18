import os
import google.generativeai as genai
import markdown
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cars.models import Cars, Categories
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

# Налаштування API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# --- ІНСТРУМЕНТИ ДЛЯ AI (Functions) ---

def get_available_cars(category_name=None, max_price=None, fuel_type=None):
    """
    Повертає список доступних автомобілів за фільтрами.
    category_name: назва категорії (наприклад, 'Економ', 'Позашляховики')
    max_price: максимальна ціна за добу
    fuel_type: тип палива ('petrol', 'diesel', 'hybrid', 'electric')
    """
    cars = Cars.objects.all()
    
    if category_name:
        cars = cars.filter(category__name__icontains=category_name)
    if max_price:
        cars = cars.filter(price__lte=max_price)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    
    result = []
    for car in cars:
        result.append({
            "id": car.id,
            "name": car.name,
            "price_per_day": float(car.price_for_sell()),
            "category": car.category.name,
            "fuel": car.get_fuel_type_display_ua(),
            "transmission": car.get_transmission_display_ua(),
            "seats": car.seats
        })
    return result if result else "На жаль, за вашим запитом авто не знайдено."

def get_car_details(car_id):
    """
    Повертає повну інформацію про конкретне авто за його ID.
    """
    try:
        car = Cars.objects.get(id=car_id)
        return {
            "name": car.name,
            "description": car.description,
            "engine": f"{car.engine_volume}л",
            "fuel_consumption": car.fuel_consumption,
            "deposit": float(car.deposit),
            "min_age": car.min_age,
            "min_experience": car.min_experience,
            "features": "Кондиціонер" if car.has_air_conditioning else "Без кондиціонера"
        }
    except Cars.DoesNotExist:
        return "Авто з таким ID не знайдено."

# --- НАЛАШТУВАННЯ МОДЕЛІ ---

# Створюємо модель з інструментами
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_available_cars, get_car_details],
    generation_config={
        "temperature": 0.5, # Менша температура для точніших відповідей
        "max_output_tokens": 1024,
    }
)

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    def post(self, request):
        user_message = request.POST.get('message', '')
        image_file = request.FILES.get('image')

        # Системна інструкція
        system_instruction = """
        Ти - експертний асистент сервісу 'Car Rental'. 
        Твоє завдання: допомогти клієнту підібрати ідеальне авто.
        
        ПРАВИЛА:
        1. Використовуй інструмент `get_available_cars`, щоб дізнатися, які авто є в наявності.
        2. Якщо клієнт зацікавився конкретним авто, використовуй `get_car_details`, щоб дати повний опис.
        3. Завжди кажи ціни та умови оренди (запорука, вік).
        4. Спілкуйся українською мовою, будь професійним та дружнім.
        5. Якщо на фото авто, яке ми маємо (або схоже), запропонуй його.
        """

        try:
            # Створюємо чат з підтримкою автоматичного виклику інструментів (enable_automatic_function_calling)
            chat = model.start_chat(enable_automatic_function_calling=True)
            
            # Формуємо запит
            content = [user_message]
            
            if image_file:
                image_data = {
                    'mime_type': image_file.content_type,
                    'data': image_file.read()
                }
                content.append(image_data)
                content.append("Клієнт надіслав фото. Перевір, чи є у нас таке авто або схоже, використовуючи інструменти пошуку.")

            # Надсилаємо повідомлення
            # Ми додаємо системну інструкцію в перший запит, якщо це початок чату
            response = chat.send_message(
                [system_instruction] + content
            )
            
            ai_reply = response.text
            ai_reply_html = markdown.markdown(ai_reply)

            return JsonResponse({'status': 'ok', 'answer': ai_reply_html})

        except Exception as e:
            print(f"Chat Error: {e}")
            return JsonResponse({
                'status': 'error',
                'answer': 'Вибачте, сталася технічна помилка. Спробуйте пізніше.'
            })
