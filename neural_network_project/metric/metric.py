import pika
import json
import csv
import os

print("=== Сервис metric (метрики) запущен ===")

# Определяем хост RabbitMQ
rabbitmq_host = 'rabbitmq'
print(f"Подключаюсь к RabbitMQ: {rabbitmq_host}")

# Пути к файлам
log_file = '/app/logs/metric_log.csv'
print(f"Файл логов: {log_file}")

# Создаем CSV файл с заголовками
if not os.path.exists(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'y_true', 'y_pred', 'absolute_error'])
    print(f" Создан файл: {log_file}")
else:
    print(f" Файл уже существует: {log_file}")

# Хранилище данных
storage = {}
processed = 0

try:
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbitmq_host)
    )
    channel = connection.channel()
    
    print(" Подключение к RabbitMQ успешно")
    
    # Проверяем/создаем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')
    
    print(" Очереди проверены")
    print("=" * 50)
    
    def process_data(msg_id, y_true=None, y_pred=None):
        global processed
        
        # Инициализируем запись если нужно
        if msg_id not in storage:
            storage[msg_id] = {'y_true': None, 'y_pred': None}
        
        # Обновляем значения
        if y_true is not None:
            storage[msg_id]['y_true'] = y_true
        if y_pred is not None:
            storage[msg_id]['y_pred'] = y_pred
        
        # Проверяем, есть ли оба значения
        if storage[msg_id]['y_true'] is not None and storage[msg_id]['y_pred'] is not None:
            y_true_val = storage[msg_id]['y_true']
            y_pred_val = storage[msg_id]['y_pred']
            error = abs(y_true_val - y_pred_val)
            
            # Записываем в CSV
            with open(log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([msg_id, y_true_val, y_pred_val, error])
            
            print(f"\n✓ Записано в CSV (ID: {msg_id}):")
            print(f"  y_true: {y_true_val:.2f}")
            print(f"  y_pred: {y_pred_val:.2f}")
            print(f"  Ошибка: {error:.2f}")
            
            # Удаляем из хранилища
            del storage[msg_id]
            processed += 1
            
            # Статистика
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"  Всего записей: {len(lines) - 1}")
            except:
                pass
            
            print("-" * 40)
    
    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            msg_id = str(data['id'])
            value = float(data['body'])
            
            # Определяем тип сообщения по очереди
            if method.routing_key == 'y_true':
                print(f"\n[y_true] ID: {msg_id}, значение: {value:.2f}")
                process_data(msg_id, y_true=value)
            elif method.routing_key == 'y_pred':
                print(f"\n[y_pred] ID: {msg_id}, значение: {value:.2f}")
                process_data(msg_id, y_pred=value)
            
            # Подтверждаем получение
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f" Ошибка: {e}")
    
    # Настраиваем потребителей
    channel.basic_qos(prefetch_count=1)
    
    # Потребитель для y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback
    )
    
    # Потребитель для y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback
    )
    
    print("Ожидание сообщений из очередей 'y_true' и 'y_pred'...")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 50)
    
    channel.start_consuming()
    
except KeyboardInterrupt:
    print(f"\n\nОстановка сервиса metric...")
    print(f"Обработано записей: {processed}")
except Exception as e:
    print(f"\n Ошибка: {e}")
finally:
    if 'connection' in locals():
        connection.close()
        print("Соединение закрыто")