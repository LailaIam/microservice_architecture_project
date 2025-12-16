Система мониторига нейронной сети в реальном времени
Микросервисная архитектура для обработки, предсказания и визуализации метрик ML-модели с использованием RabbitMQ, Docker и Python.

Особенности
Микросервисная архитектура на базе RabbitMQ

Обмен сообщениями в реальном времени через AMQP

Автоматическое логирование метрик в CSV

Визуализация ошибок с автообновлением графика

Полная контейнеризация через Docker Compose

Уникальные идентификаторы для трассировки сообщений

Архитектура системы
text
[features] → (features, y_true) → [RabbitMQ] → [model] → y_pred → [RabbitMQ]
                                                              ↓
[metric] ← (y_true, y_pred) ← [RabbitMQ] → запись в CSV → [plot] → гистограмма PNG
Технологический стек
Язык: Python 3.9

Брокер сообщений: RabbitMQ 3-management

Контейнеризация: Docker + Docker Compose

Визуализация: Matplotlib, Pandas

ML-библиотеки: Scikit-learn, NumPy

Протокол: AMQP (pika)

Структура проекта
text
neural_network_project/
├── docker-compose.yml          # Конфигурация Docker
├── requirements.txt            # Зависимости Python
├── logs/                       # Результаты работы
│   ├── metric_log.csv          # CSV с метриками
│   └── error_distribution.png  # Гистограмма ошибок
├── features/                   # Генератор данных
│   ├── features.py            # Задержка 10 сек + ID
│   └── Dockerfile
├── model/                      # Модель предсказаний
│   ├── model.py               # Предсказания
│   └── Dockerfile
├── metric/                     # Сервис метрик
│   ├── metric.py              # Запись в CSV
│   └── Dockerfile
└── plot/                       # Визуализация
    ├── plot.py                # Гистограмма
    └── Dockerfile
Быстрый старт
1. Клонирование репозитория
bash
git clone https://github.com/ваш-username/neural-network-monitoring.git
cd neural-network-monitoring
2. Запуск системы
bash
docker-compose up --build
3. Проверка работы
bash
# Просмотр логов
docker-compose logs -f features

# Проверка файлов
cat logs/metric_log.csv
4. Доступ к интерфейсам
RabbitMQ Management: http://localhost:15672 (guest/guest)

График ошибок: logs/error_distribution.png

Критерии выполнения
Обмен сообщениями через AMQP - RabbitMQ + 4 сервиса

Временная задержка в features - 10 секунд между итерациями

Уникальные идентификаторы - ID совпадают для y_true и y_pred

Запись в metric_log.csv - CSV файл с метриками

Построение гистограммы ошибок - PNG файл с распределением

Что делает каждый сервис
features
Загружает diabetes dataset из scikit-learn

Генерирует уникальные ID для сообщений

Отправляет признаки в очередь features

Отправляет истинные значения в очередь y_true

Задержка 10 секунд между итерациями

model
Читает признаки из очереди features

Делает предсказания (линейная модель)

Отправляет предсказания в очередь y_pred

metric
Читает сообщения из y_true и y_pred

Сопоставляет данные по ID

Вычисляет абсолютные ошибки

Записывает результаты в metric_log.csv

plot
Читает данные из metric_log.csv

Строит гистограмму распределения ошибок

Сохраняет график в error_distribution.png

Обновляется каждые 10 секунд

Пример данных
metric_log.csv
csv
id,y_true,y_pred,absolute_error
1765912012.233366,101.0,116.95,15.95
1765912022.240461,103.0,133.72,30.72
1765912032.250322,235.0,142.59,92.41
Гистограмма ошибок
https://logs/error_distribution.png

Команды управления
bash
# Запуск всей системы
docker-compose up -d

# Остановка системы
docker-compose down

# Просмотр логов конкретного сервиса
docker-compose logs -f features
docker-compose logs -f metric
docker-compose logs -f plot

# Пересборка конкретного сервиса
docker-compose build features

# Полная очистка
docker-compose down --volumes --rmi all
Используемые датасеты
Diabetes dataset из scikit-learn

442 samples, 10 features

Целевая переменная: quantitative measure of disease progression

Мониторинг
RabbitMQ Queues
features - векторы признаков

y_true - истинные значения

y_pred - предсказания модели

Файлы мониторинга
logs/metric_log.csv - история всех предсказаний

logs/error_distribution.png - визуализация ошибок

Отладка
bash
# Проверка подключения к RabbitMQ
docker-compose logs rabbitmq

# Проверка очередей
curl -u guest:guest http://localhost:15672/api/queues

# Просмотр логов всех сервисов
docker-compose logs --tail=50
Лицензия
MIT License

Автор
[Ваше Имя] - учебный проект по нейронным сетям
