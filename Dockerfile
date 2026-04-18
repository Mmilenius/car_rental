# Використовуємо ПОВНИЙ образ Python (він більший, але стабільний і вже має всі інструменти)
FROM python:3.10-bookworm

# Налаштування змінного середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Створюємо робочу директорію
WORKDIR /app

# Оскільки ми використовуємо повний образ, нам НЕ ПОТРІБНО ставити build-essential, 
# він там уже є. Це дозволить уникнути помилки Hash Sum mismatch.

# Копіюємо файл залежностей і встановлюємо їх
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект
COPY . /app/

# Відкриваємо порт
EXPOSE 8000

# Запуск
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
