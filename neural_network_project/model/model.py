import pika
import json
import numpy as np
import sys
import os

print("=== Сервис model (предсказания) запущен ===")

def make_prediction(features):
    """
    Реалистичная модель для предсказания diabetes progression.
    Возвращает значения в диапазоне ~50-300.
    """
    # Коэффициенты (имитация обученной модели)
    coefficients = np.array([
        42.8, 31.5, 28.9, 19.6, 35.2,
        27.4, 33.1, 24.8, 29.7, 38.5
    ])
    
    # Преобразуем признаки в numpy array
    features_array = np.array(features)
    
    # Линейная комбинация
    prediction = np.dot(features_array, coefficients) + 125.0
    
    # Добавляем реалистичный шум
    noise = np.random.normal(0, 18)
    prediction += noise
    
    # Ограничиваем диапазоном diabetes target (25-350)
    prediction = np.clip(prediction, 50, 300)
    
    return float(prediction)

# Определяем хост RabbitMQ
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

    # Создание очередей (если не существуют)
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')

    print(" Подключение к RabbitMQ успешно")
    print(" Очереди созданы/проверены")
    print("=" * 50)

    def callback(ch, method, properties, body):
        """Обработчик входящих сообщений с признаками"""
        try:
            # Десериализация сообщения
            message = json.loads(body)
            msg_id = message['id']
            features = message['body']
            
            print(f"\nПолучены признаки (ID: {msg_id}):")
            print(f"Количество признаков: {len(features)}")
            
            # Делаем предсказание
            prediction = make_prediction(features)
            
            # Формируем сообщение с предсказанием
            message_pred = {
                'id': msg_id,
                'body': prediction
            }
            
            # Отправляем предсказание в очередь y_pred
            channel.basic_publish(
                exchange='',
                routing_key='y_pred',
                body=json.dumps(message_pred)
            )
            
            print(f" Предсказание: {prediction:.2f}")
            print("-" * 40)
            
            # Подтверждаем получение сообщения
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f" Ошибка обработки: {type(e).__name__}: {e}")

    # Настройка потребителя
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='features',
        on_message_callback=callback
    )

    print("Ожидание сообщений из очереди 'features'...")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 50)

    # Начинаем потребление сообщений
    channel.start_consuming()

except KeyboardInterrupt:
    print("\n\nОстановка сервиса model...")
except pika.exceptions.AMQPConnectionError as e:
    print(f"\n✗ Ошибка подключения к RabbitMQ: {e}")
    print(f"\nПроверьте, что RabbitMQ запущен:")
    print("docker-compose ps")
except Exception as e:
    print(f"\nОшибка: {type(e).__name__}: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()
        print("Соединение с RabbitMQ закрыто")