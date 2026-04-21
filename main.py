"""
Главный модуль приложения для мониторинга воздушных судов.
Обеспечивает взаимодействие с пользователем через консоль.
"""

import logging
from typing import List, Optional

from src.aeroplane import Aeroplane
from src.api_classes import AviationAPI
from src.file_classes import JSONStorage
from src.utils import (
    filter_by_altitude_range,
    filter_by_country,
    get_top_n_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes_by_altitude,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем.
    Реализует консольный интерфейс для работы с данными о самолетах.
    """
    print("\n" + "=" * 70)
    print("🛩️  ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ МОНИТОРИНГА ВОЗДУШНЫХ СУДОВ 🛩️")
    print("=" * 70)

    # Инициализация компонентов
    api = AviationAPI()
    storage = JSONStorage()

    # Шаг 1: Ввод названия страны
    country = input("\n🌍 Введите название страны для поиска самолетов: ").strip()
    if not country:
        print("❌ Название страны не может быть пустым!")
        return

    print(f"\n🔍 Получение информации о самолетах в воздушном пространстве {country}...")

    # Получаем данные через API
    aeroplanes_data = api.get_aeroplanes(country)

    if not aeroplanes_data:
        print(f"⚠️ Не удалось получить данные о самолетах для {country}.")
        print("   Возможные причины: страна не найдена или в воздушном пространстве нет самолетов.")
        return

    # Преобразуем в объекты Aeroplane
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)
    print(f"✅ Получено {len(aeroplanes)} самолетов!")

    # Сохраняем в файл
    saved_count = 0
    for aeroplane in aeroplanes:
        if storage.add_aeroplane(aeroplane.to_dict()):
            saved_count += 1
    print(f"💾 Сохранено в файл: {saved_count} новых самолетов")

    # Шаг 2: Топ N по высоте
    print("\n" + "-" * 50)
    print("📊 ФИЛЬТРАЦИЯ И СОРТИРОВКА ДАННЫХ")
    print("-" * 50)

    try:
        top_n_input = input("✈️ Введите количество самолетов для вывода в топ (например, 10): ").strip()
        top_n = int(top_n_input) if top_n_input else 10
    except ValueError:
        print("❌ Неверный ввод. Будет использовано значение по умолчанию (10)")
        top_n = 10

    # Сортируем по высоте и получаем топ
    sorted_by_altitude = sort_aeroplanes_by_altitude(aeroplanes, reverse=True)
    top_aeroplanes = get_top_n_aeroplanes(sorted_by_altitude, top_n)

    print_aeroplanes(top_aeroplanes, f"ТОП-{top_n} ПО ВЫСОТЕ ПОЛЕТА")

    # Шаг 3: Фильтрация по стране регистрации
    countries_input = input("\n🌍 Введите страны для фильтрации через пробел (или Enter для пропуска): ").strip()
    if countries_input:
        filter_countries = [c.strip() for c in countries_input.split()]
        filtered_by_country = filter_by_country(aeroplanes, filter_countries)
        print_aeroplanes(filtered_by_country, f"САМОЛЕТЫ ИЗ СТРАН {filter_countries}")

    # Шаг 4: Фильтрация по диапазону высот
    altitude_input = input("\n📏 Введите диапазон высот (например: 1000-5000, 10000, или Enter для пропуска): ").strip()
    if altitude_input:
        try:
            if "-" in altitude_input:
                parts = altitude_input.split("-")
                min_alt = float(parts[0]) if parts[0] else None
                max_alt = float(parts[1]) if parts[1] else None
            else:
                min_alt = None
                max_alt = float(altitude_input)

            filtered_by_altitude = filter_by_altitude_range(aeroplanes, min_alt, max_alt)
            print_aeroplanes(filtered_by_altitude, f"САМОЛЕТЫ В ДИАПАЗОНЕ ВЫСОТ {altitude_input}")
        except ValueError:
            print("❌ Неверный формат диапазона высот")

    # Дополнительно: показать статистику из файла
    print("\n" + "-" * 50)
    print("📈 СТАТИСТИКА ПО СОХРАНЕННЫМ ДАННЫМ")
    print("-" * 50)
    stats = storage.get_statistics()
    print(f"📊 Всего сохранено самолетов: {stats['total']}")
    print(f"🌍 Уникальных стран: {len(stats['countries'])}")
    print(f"📏 Средняя высота: {stats['avg_altitude']:.0f} м")
    print(f"⚡ Средняя скорость: {stats['avg_velocity']:.1f} м/с")
    print(f"🛬 На земле: {stats['on_ground_count']}")
    print(f"🛫 В воздухе: {stats['in_air_count']}")


def main() -> None:
    """Точка входа в программу."""
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем. До свидания!")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        print(f"\n❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
