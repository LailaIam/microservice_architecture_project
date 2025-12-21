FROM python:3.9-slim

WORKDIR /app

# Создаем папку для логов
RUN mkdir -p /app/logs

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY metric.py .

# Запускаем сервис
CMD ["python", "metric.py"]