FROM python:3.9-slim

WORKDIR /app

# Устанавливаем системные зависимости для matplotlib
RUN apt-get update && apt-get install -y \
    libfreetype6 \
    libpng16-16 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY plot.py .

# Создаем папку для логов
RUN mkdir -p /app/logs

# Запускаем сервис
CMD ["python", "plot.py"]