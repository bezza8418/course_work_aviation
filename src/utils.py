"""
Модуль со вспомогательными функциями для работы с данными о самолетах.
Содержит функции фильтрации, сортировки и вывода информации.
"""

import logging
from typing import List, Optional

from src.aeroplane import Aeroplane

logger = logging.getLogger(__name__)


def sort_aeroplanes_by_altitude(
    aeroplanes: List[Aeroplane], reverse: bool = True
) -> List[Aeroplane]:
    """
    Сортировка списка самолетов по высоте полета.

    Args:
        aeroplanes: Список объектов Aeroplane
        reverse: True для сортировки по убыванию, False для возрастания

    Returns:
        List[Aeroplane]: Отсортированный список самолетов
    """
    return sorted(aeroplanes, key=lambda a: a.altitude, reverse=reverse)


def sort_aeroplanes_by_velocity(
    aeroplanes: List[Aeroplane], reverse: bool = True
) -> List[Aeroplane]:
    """
    Сортировка списка самолетов по скорости.

    Args:
        aeroplanes: Список объектов Aeroplane
        reverse: True для сортировки по убыванию, False для возрастания

    Returns:
        List[Aeroplane]: Отсортированный список самолетов
    """
    return sorted(aeroplanes, key=lambda a: a.velocity, reverse=reverse)


def get_top_n_aeroplanes(
    aeroplanes: List[Aeroplane], top_n: int
) -> List[Aeroplane]:
    """
    Получение топ N самолетов.

    Args:
        aeroplanes: Список объектов Aeroplane (предполагается, что уже отсортирован)
        top_n: Количество самолетов для возврата

    Returns:
        List[Aeroplane]: Первые top_n самолетов из списка
    """
    return aeroplanes[:top_n]


def filter_by_country(
    aeroplanes: List[Aeroplane], countries: List[str]
) -> List[Aeroplane]:
    """
    Фильтрация самолетов по стране регистрации.

    Args:
        aeroplanes: Список объектов Aeroplane
        countries: Список стран для фильтрации

    Returns:
        List[Aeroplane]: Отфильтрованный список самолетов
    """
    if not countries:
        return aeroplanes

    filtered = []
    for aeroplane in aeroplanes:
        if aeroplane.origin_country in countries:
            filtered.append(aeroplane)

    logger.info(f"Отфильтровано {len(filtered)} самолетов по странам {countries}")
    return filtered


def filter_by_altitude_range(
    aeroplanes: List[Aeroplane],
    min_altitude: Optional[float] = None,
    max_altitude: Optional[float] = None
) -> List[Aeroplane]:
    """
    Фильтрация самолетов по диапазону высот.

    Args:
        aeroplanes: Список объектов Aeroplane
        min_altitude: Минимальная высота (None - без ограничения)
        max_altitude: Максимальная высота (None - без ограничения)

    Returns:
        List[Aeroplane]: Отфильтрованный список самолетов
    """
    filtered = []
    for aeroplane in aeroplanes:
        if min_altitude is not None and aeroplane.altitude < min_altitude:
            continue
        if max_altitude is not None and aeroplane.altitude > max_altitude:
            continue
        filtered.append(aeroplane)

    logger.info(f"Отфильтровано {len(filtered)} самолетов по диапазону высот")
    return filtered


def filter_by_velocity_range(
    aeroplanes: List[Aeroplane],
    min_velocity: Optional[float] = None,
    max_velocity: Optional[float] = None
) -> List[Aeroplane]:
    """
    Фильтрация самолетов по диапазону скоростей.

    Args:
        aeroplanes: Список объектов Aeroplane
        min_velocity: Минимальная скорость (None - без ограничения)
        max_velocity: Максимальная скорость (None - без ограничения)

    Returns:
        List[Aeroplane]: Отфильтрованный список самолетов
    """
    filtered = []
    for aeroplane in aeroplanes:
        if min_velocity is not None and aeroplane.velocity < min_velocity:
            continue
        if max_velocity is not None and aeroplane.velocity > max_velocity:
            continue
        filtered.append(aeroplane)

    logger.info(f"Отфильтровано {len(filtered)} самолетов по диапазону скоростей")
    return filtered


def print_aeroplanes(aeroplanes: List[Aeroplane], title: str = "САМОЛЕТЫ") -> None:
    """
    Красивый вывод информации о самолетах в консоль.

    Args:
        aeroplanes: Список объектов Aeroplane
        title: Заголовок таблицы
    """
    if not aeroplanes:
        print("\n❌ Самолеты не найдены.")
        return

    print("\n" + "=" * 110)
    print(f"📊 {title}")
    print("=" * 110)
    print(f"{'Позывной':<12} {'Страна':<25} {'Скорость (м/с)':<15} {'Высота (м)':<12} {'На земле':<10}")
    print("-" * 110)

    for a in aeroplanes:
        on_ground = "Да" if a.on_ground else "Нет"
        print(f"{a.callsign:<12} {a.origin_country:<25} {a.velocity:<15.1f} {a.altitude:<12.0f} {on_ground:<10}")

    print("=" * 110)
    print(f"📈 Всего: {len(aeroplanes)} самолетов")


def parse_altitude_range(altitude_input: str) -> tuple[Optional[float], Optional[float]]:
    """
    Парсинг введенного пользователем диапазона высот.

    Args:
        altitude_input: Строка с диапазоном (например, "1000-5000", "2000" или "до 3000")

    Returns:
        tuple[Optional[float], Optional[float]]: (min_altitude, max_altitude)
    """
    if not altitude_input or altitude_input.strip() == "":
        return None, None

    altitude_input = altitude_input.replace(" ", "")

    if "-" in altitude_input:
        parts = altitude_input.split("-")
        min_alt = float(parts[0]) if parts[0] else None
        max_alt = float(parts[1]) if parts[1] else None
        return min_alt, max_alt
    else:
        # Если указано одно значение - это максимальная высота
        return None, float(altitude_input)
