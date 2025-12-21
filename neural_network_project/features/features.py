import pika
import json
import time
import numpy as np
from datetime import datetime
from sklearn.datasets import load_diabetes
import sys
import os

print("=== Сервис features запущен ===")

# Загрузка датасета
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

print(f"Загружен датасет: {X.shape[0]} samples, {X.shape[1]} features")

# Определяем хост RabbitMQ
# В Docker Compose используем имя сервиса 'rabbitmq', локально 'localhost'
if os.environ.get('DOCKER_COMPOSE') == 'true':
    rabbitmq_host = 'rabbitmq'
    print("Режим: Docker Compose (подключение к 'rabbitmq')")
else:
    rabbitmq_host = 'localhost'
    print("Режим: Локальный запуск (подключение к 'localhost')")

print(f"Подключаюсь к RabbitMQ на хосте: {rabbitmq_host}")

try:
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            rabbitmq_host,
            connection_attempts=5,
            retry_delay=3
        )
    )
    channel = connection.channel()

    # Создание очередей
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    print(" Подключение к RabbitMQ успешно")
    print(" Очереди созданы/проверены")
    print("=" * 50)

    iteration = 1

    while True:
        # 1. Выбор случайной строки
        random_row = np.random.randint(0, X.shape[0])
        
        # 2. Генерация уникального ID
        message_id = datetime.timestamp(datetime.now())
        
        print(f"\nИтерация {iteration}:")
        print(f"ID: {message_id}")
        print(f"Выбрана строка: {random_row}")
        
        # 3. Формирование сообщения с признаками
        message_features = {
            'id': message_id,
            'body': X[random_row].tolist()
        }
        
        # 4. Формирование сообщения с истинным ответом
        message_y_true = {
            'id': message_id,
            'body': float(y[random_row])
        }
        
        # 5. Отправка в очередь features
        channel.basic_publish(
            exchange='',
            routing_key='features',
            body=json.dumps(message_features)
        )
        print(f" Отправлено в 'features': {len(message_features['body'])} признаков")
        
        # 6. Отправка в очередь y_true
        channel.basic_publish(
            exchange='',
            routing_key='y_true',
            body=json.dumps(message_y_true)
        )
        print(f" Отправлено в 'y_true': {message_y_true['body']:.2f}")
        
        # 7. Задержка между итерациями
        delay_time = 10
        print(f" Жду {delay_time} секунд...")
        time.sleep(delay_time)
        
        iteration += 1
        
except KeyboardInterrupt:
    print("\n\nОстановка сервиса features...")
except pika.exceptions.AMQPConnectionError as e:
    print(f"\n Ошибка подключения к RabbitMQ: {e}")
    print(f"\nПроверьте:")
    print("1. RabbitMQ запущен в Docker Compose?")
    print("2. Хост: {rabbitmq_host}")
    print("3. Команда проверки: docker-compose ps")
except Exception as e:
    print(f"\nОшибка: {type(e).__name__}: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()
        print("Соединение с RabbitMQ закрыто")