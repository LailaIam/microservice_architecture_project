FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY model.py .

# Запускаем сервис
CMD ["python", "model.py"]