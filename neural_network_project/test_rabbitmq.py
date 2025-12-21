import pika
import json

print("Подключаемся к RabbitMQ...")

try:
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    
    # Создание очередей
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')
    
    # Тестовое сообщение
    test_message = {
        'id': 123.456,
        'body': [1.0, 2.0, 3.0]
    }
    
    # Отправка сообщения
    channel.basic_publish(
        exchange='',
        routing_key='features',
        body=json.dumps(test_message)
    )
    
    print("Сообщение отправлено в очередь 'features'")
    print(f"Сообщение: {test_message}")
    
    # Закрытие соединения
    connection.close()
    
    print("\nПроверьте в браузере:")
    print("1. Откройте http://localhost:15672")
    print("2. Логин: guest, Пароль: guest")
    print("3. Перейдите на вкладку Queues")
    print("4. Должна быть очередь 'features' с 1 сообщением")
    
except Exception as e:
    print(f"Ошибка: {e}")
    print("\nВозможные причины:")
    print("1. Docker Desktop не запущен")
    print("2. Контейнер rabbitmq не запущен")
    print("3. Порт 5672 занят")
    input("Нажмите Enter для выхода...")