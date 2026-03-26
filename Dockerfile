FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Сначала копируем только requirements.txt для кэширования
COPY requirements.txt .

# Установка зависимостей
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]