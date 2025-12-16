# Система мониторинга нейронной сети в реальном времени
Микросервисная архитектура для обработки, предсказания и визуализации метрик ML-модели с использованием RabbitMQ, Docker и Python.
# Особенности
Микросервисная архитектура на базе RabbitMQ

Обмен сообщениями в реальном времени через AMQP

Автоматическое логирование метрик в CSV

Визуализация ошибок с автообновлением графика

Полная контейнеризация через Docker Compose

Уникальные идентификаторы для трассировки сообщений
# Архитектура
[features] → (features, y_true) → [RabbitMQ] → [model] → y_pred → [RabbitMQ]
                                                              ↓
[metric] ← (y_true, y_pred) ← [RabbitMQ] → запись в CSV → [plot] → гистограмма PNG
# Технологический стек
Технология	Назначение
Python 3.9	Основной язык программирования
RabbitMQ 3-management	Брокер сообщений
Docker + Docker Compose	Контейнеризация и оркестрация
Matplotlib, Pandas	Визуализация и анализ данных
Scikit-learn, NumPy	ML и работа с данными
AMQP (pika)	Протокол обмена сообщениями
# Структура проекта
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
    
