"""
Модуль с классами для работы с внешними API.
Реализует взаимодействие с Nominatim (геокодирование) и OpenSky (данные о самолетах).
"""

import logging
from typing import Any, Dict, List, Optional

import requests

from src.abstract_classes import BaseAPI

# User-Agent для идентификации приложения при запросах к API
APP_USER_AGENT = "CourseWorkAviationApp/1.0 (coursework; student@example.com)"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AviationAPI(BaseAPI):
    """
    Класс для работы с API Nominatim и OpenSky.
    Получает географические координаты стран и информацию о самолетах.
    """

    def __init__(self) -> None:
        """Инициализация API для работы с авиационными данными."""
        super().__init__(base_url="")
        self._nominatim_url: str = "https://nominatim.openstreetmap.org/search"
        self._opensky_url: str = "https://opensky-network.org/api/states/all"
        self._connected: bool = False

    def _connect(self) -> bool:
        """
        Проверка доступности API сервисов.

        Returns:
            bool: True если сервисы доступны, иначе False
        """
        try:
            # Проверяем доступность Nominatim
            headers = {"User-Agent": APP_USER_AGENT}
            params = {"q": "test", "format": "json", "limit": 1}
            response = requests.get(
                self._nominatim_url, headers=headers, params=params, timeout=10
            )
            if response.status_code != 200:
                logger.error(f"❌ Nominatim недоступен: {response.status_code}")
                self._connected = False
                return False

            # Проверяем доступность OpenSky
            response = requests.get(self._opensky_url, timeout=10)
            if response.status_code != 200:
                logger.error(f"❌ OpenSky недоступен: {response.status_code}")
                self._connected = False
                return False

            self._connected = True
            logger.info("✅ Все API сервисы доступны")
            return True

        except requests.RequestException as e:
            logger.error(f"❌ Ошибка соединения: {e}")
            self._connected = False
            return False

    def get_country_bounding_box(self, country: str) -> Optional[List[float]]:
        """
        Получение bounding box страны через Nominatim API.

        Args:
            country: Название страны (например, "Russia", "Spain", "France")

        Returns:
            Optional[List[float]]: [юг, север, запад, восток] или None при ошибке
        """
        if not self._connected:
            self._connect()

        try:
            params: dict[str, str | int] = {
                "q": country,
                "format": "json",
                "limit": 1,
                "polygon_geojson": 0,
            }

            logger.info(f"🌍 Запрос координат для страны: {country}")
            response = requests.get(self._nominatim_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    bounding_box = data[0].get("boundingbox", [])
                    if bounding_box:
                        # Преобразуем строки в числа
                        result: List[float] = [float(coord) for coord in bounding_box]
                        logger.info(f"📍 Bounding box для {country}: {result}")
                        return result
                    else:
                        logger.warning(f"⚠️ Bounding box для {country} не найден")
                else:
                    logger.warning(f"⚠️ Страна {country} не найдена")
            else:
                logger.error(f"❌ Ошибка запроса к Nominatim: {response.status_code}")

        except requests.RequestException as e:
            logger.error(f"❌ Ошибка при запросе к Nominatim: {e}")

        return None

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах для указанной страны через OpenSky API.

        Args:
            country: Название страны

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о самолетах
        """
        # Проверяем подключение к API
        if not self._connected and not self._connect():
            logger.error("❌ Нет подключения к API сервисам")
            return []

        # Получаем bounding box страны
        bbox = self.get_country_bounding_box(country)

        if not bbox:
            logger.warning(f"⚠️ Не удалось получить bounding box для {country}")
            return []

        # Параметры запроса: bounding box (юг, север, запад, восток)
        params: dict[str, float] = {
            "lamin": bbox[0],  # юг (минимальная широта)
            "lamax": bbox[1],  # север (максимальная широта)
            "lomin": bbox[2],  # запад (минимальная долгота)
            "lomax": bbox[3],  # восток (максимальная долгота)
        }

        logger.info(f"🛩️ Запрос данных о самолетах для {country}")

        try:
            response = requests.get(self._opensky_url, params=params, timeout=15)

            if response.status_code == 200:
                data = response.json()
                states = data.get("states", [])

                if not states:
                    logger.info(f"ℹ️ В воздушном пространстве {country} нет самолетов")
                    return []

                # Преобразуем данные в удобный формат словарей
                aeroplanes_data: List[Dict[str, Any]] = []
                for state in states:
                    # Формат данных OpenSky (индексы массива):
                    # 0: icao24, 1: callsign, 2: origin_country, 3: time_position,
                    # 4: last_contact, 5: longitude, 6: latitude, 7: baro_altitude,
                    # 8: on_ground, 9: velocity, 10: true_track, 11: vertical_rate,
                    # 12: sensors, 13: geo_altitude, 14: squawk, 15: spi, 16: position_source
                    aeroplane_dict: Dict[str, Any] = {
                        "icao24": state[0],
                        "callsign": state[1].strip() if state[1] else "N/A",
                        "origin_country": state[2],
                        "longitude": state[5],
                        "latitude": state[6],
                        "altitude": state[7] if state[7] is not None else 0,
                        "on_ground": state[8],
                        "velocity": state[9] if state[9] is not None else 0,
                        "true_track": state[10],
                        "vertical_rate": state[11],
                        "geo_altitude": state[13] if state[13] is not None else 0,
                    }
                    aeroplanes_data.append(aeroplane_dict)

                logger.info(
                    f"✅ Получено {len(aeroplanes_data)} самолетов для {country}"
                )
                return aeroplanes_data

            else:
                logger.error(f"❌ Ошибка OpenSky API: {response.status_code}")
                return []

        except requests.RequestException as e:
            logger.error(f"❌ Ошибка запроса к OpenSky: {e}")
            return []
