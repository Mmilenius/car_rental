import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cars.models import Cars, Categories
from dotenv import load_dotenv

# Спробуємо імпортувати бібліотеки безпечно
try:
    import markdown
except ImportError:
    markdown = None

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

# Завантажуємо змінні з .env
load_dotenv()

# Налаштування API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
client = None
if genai and GENAI_API_KEY:
    client = genai.Client(api_key=GENAI_API_KEY)

# --- ІНСТРУМЕНТИ ДЛЯ AI (Functions) ---

def get_available_cars(category_name: str = None, max_price: float = None, fuel_type: str = None):
    """Повертає список доступних автомобілів за фільтрами."""
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

def get_car_details(car_id: int):
    """Повертає повну інформацію про конкретне авто."""
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

tools = [get_available_cars, get_car_details]

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    def post(self, request):
        if not client:
            return JsonResponse({'status': 'error', 'answer': 'AI-сервіс не налаштований (відсутній ключ або бібліотеки).'})

        user_message = request.POST.get('message', '')
        image_file = request.FILES.get('image')

        # Отримуємо або ініціалізуємо історію з сесії
        history = request.session.get('chat_history', [])

        system_instruction = """
        Ти - експертний асистент сервісу 'Car Rental'. 
        Твоє завдання: допомогти клієнту підібрати ідеальне авто, використовуючи доступні інструменти.
        
        ПРАВИЛА:
        1. Якщо клієнт надає параметри (тип кузова, бюджет, паливо), НЕГАЙНО викликай функцію `get_available_cars`.
        2. Якщо клієнт питає про конкретне авто, використовуй `get_car_details`.
        3. Якщо клієнт просить "економічне" авто, шукай у категорії "Бюджетні" або з низькою ціною.
        4. Не вітайся кожного разу, якщо діалог уже триває.
        5. Спілкуйся українською мовою.
        6. Якщо у відповіді від інструментів є список авто, красиво оформи його маркдауном.
        """

        try:
            # Формуємо контент для поточного запиту
            current_content = {"role": "user", "parts": [{"text": user_message}]}
            
            if image_file:
                image_bytes = image_file.read()
                current_content["parts"].append(
                    types.Part.from_bytes(data=image_bytes, mime_type=image_file.content_type)
                )

            # Формуємо повний список повідомлень для моделі
            messages = []
            for msg in history:
                messages.append(types.Content(role=msg['role'], parts=[types.Part(text=msg['text'])]))
            
            # Додаємо поточне повідомлення (без картинки для простоти збереження в сесії, або з нею якщо треба)
            # Але в SDK ми передаємо об'єкти Content
            current_parts = [types.Part(text=user_message)]
            if image_file:
                current_parts.append(types.Part.from_bytes(data=image_bytes, mime_type=image_file.content_type))
            
            messages.append(types.Content(role="user", parts=current_parts))

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(),
                ),
            )
            
            ai_reply = response.text
            
            # Оновлюємо історію в сесії (зберігаємо лише текст для економії місця)
            history.append({"role": "user", "text": user_message})
            history.append({"role": "model", "text": ai_reply})
            
            # Обмежуємо історію останніми 10 повідомленнями
            request.session['chat_history'] = history[-10:]

            if markdown:
                ai_reply_html = markdown.markdown(ai_reply)
            else:
                ai_reply_html = ai_reply

            return JsonResponse({'status': 'ok', 'answer': ai_reply_html})

        except Exception as e:
            print(f"Chat Error: {e}")
            return JsonResponse({'status': 'error', 'answer': f'Помилка: {str(e)}'})
