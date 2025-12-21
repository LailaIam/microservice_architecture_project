import pandas as pd
import matplotlib.pyplot as plt
import time
import os

print("=== Сервис plot (визуализация) запущен ===")

# Пути к файлам (внутри Docker контейнера)
csv_file = '/app/logs/metric_log.csv'
plot_file = '/app/logs/error_distribution.png'

print(f"Файл данных: {csv_file}")
print(f"Файл графика: {plot_file}")

# Создаем папку logs, если её нет
log_dir = os.path.dirname(csv_file)
os.makedirs(log_dir, exist_ok=True)
print(f"Папка логов проверена: {log_dir}")

# Счетчик итераций
iteration = 0
update_interval = 10  # секунд между обновлениями

try:
    while True:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"Итерация {iteration}: {time.strftime('%H:%M:%S')}")
        print(f"Проверяю файл: {csv_file}")
        
        # Проверяем, существует ли файл с данными
        if not os.path.exists(csv_file):
            print("Файл metric_log.csv не найден. Жду данные...")
            time.sleep(update_interval)
            continue
        
        try:
            # Читаем CSV файл
            df = pd.read_csv(csv_file)
            
            # Проверяем, есть ли данные (кроме заголовка)
            if len(df) == 0:
                print("CSV файл пуст. Жду данные...")
                time.sleep(update_interval)
                continue
            
            print(f"Загружено строк: {len(df)}")
            print(f"Диапазон ошибок: {df['absolute_error'].min():.2f} - {df['absolute_error'].max():.2f}")
            print(f"Средняя ошибка: {df['absolute_error'].mean():.2f}")
            
            # Создаем гистограмму
            plt.figure(figsize=(12, 6))
            
            # Основная гистограмма
            plt.hist(
                df['absolute_error'], 
                bins=20, 
                edgecolor='black', 
                alpha=0.7,
                color='skyblue'
            )
            
            # Добавляем вертикальную линию для среднего значения
            mean_error = df['absolute_error'].mean()
            plt.axvline(
                x=mean_error, 
                color='red', 
                linestyle='--', 
                linewidth=2,
                label=f'Среднее: {mean_error:.2f}'
            )
            
            # Добавляем медиану
            median_error = df['absolute_error'].median()
            plt.axvline(
                x=median_error, 
                color='green', 
                linestyle=':', 
                linewidth=2,
                label=f'Медиана: {median_error:.2f}'
            )
            
            # Настройки графика
            plt.title(f'Распределение абсолютных ошибок модели\nВсего наблюдений: {len(df)}', fontsize=14, pad=20)
            plt.xlabel('Абсолютная ошибка', fontsize=12)
            plt.ylabel('Частота', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Добавляем текстовую информацию
            stats_text = (
                f"Мин: {df['absolute_error'].min():.2f}\n"
                f"Макс: {df['absolute_error'].max():.2f}\n"
                f"Срдн: {df['absolute_error'].mean():.2f}\n"
                f"Стд: {df['absolute_error'].std():.2f}"
            )
            plt.text(
                0.95, 0.95, stats_text,
                transform=plt.gca().transAxes,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
            )
            
            # Сохраняем график
            plt.tight_layout()
            plt.savefig(plot_file, dpi=150, bbox_inches='tight')
            plt.close()  # Закрываем график, чтобы не накапливать в памяти
            
            print(f" Гистограмма сохранена: {plot_file}")
            
            # Показываем текущие данные
            if len(df) > 0:
                print("\nПоследние 5 записей:")
                print(df[['id', 'y_true', 'y_pred', 'absolute_error']].tail())
            
        except pd.errors.EmptyDataError:
            print("CSV файл пуст или содержит только заголовок")
        except KeyError as e:
            print(f"Ошибка: в CSV файле отсутствует столбец {e}")
            print("Ожидаемые столбцы: id, y_true, y_pred, absolute_error")
        except Exception as e:
            print(f"Ошибка обработки данных: {type(e).__name__}: {e}")
        
        print(f"\nЖду {update_interval} секунд до следующего обновления...")
        time.sleep(update_interval)

except KeyboardInterrupt:
    print("\n\nОстановка сервиса plot...")
    print(f"Всего итераций: {iteration}")
except Exception as e:
    print(f"\nКритическая ошибка: {type(e).__name__}: {e}")