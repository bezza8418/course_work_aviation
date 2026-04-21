"""
Модуль с классами для работы с файловым хранилищем.
Реализует сохранение, загрузку и удаление данных о самолетах в JSON-формате.
"""

import json
import logging
import os
from typing import Any, Dict, List

from src.abstract_classes import BaseFileStorage

logger = logging.getLogger(__name__)


class JSONStorage(BaseFileStorage):
    """
    Класс для работы с JSON-файлом как хранилищем данных о самолетах.

    Атрибуты:
        _filename: Имя файла для хранения данных (приватный)
    """

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        """
        Инициализация JSON хранилища.

        Args:
            filename: Имя файла для хранения данных (по умолчанию: data/aeroplanes.json)
        """
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Приватный метод: создает директорию и файл, если они не существуют.
        """
        directory = os.path.dirname(self._filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"📁 Создана директория: {directory}")

        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            logger.info(f"📄 Создан файл: {self._filename}")

    def _load_data(self) -> List[Dict[str, Any]]:
        """
        Приватный метод: загружает данные из JSON-файла.

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о самолетах
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"❌ Ошибка загрузки данных: {e}")
            return []

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Приватный метод: сохраняет данные в JSON-файл.

        Args:
            data: Список словарей для сохранения
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _is_duplicate(
        aeroplane_data: Dict[str, Any], existing_data: List[Dict[str, Any]]
    ) -> bool:
        """
        Приватный метод: проверяет наличие дубликата по уникальным полям.

        Args:
            aeroplane_data: Данные нового самолета
            existing_data: Существующие данные в файле

        Returns:
            bool: True если дубликат найден, иначе False
        """
        for existing in existing_data:
            # Сравниваем по позывному и ICAO24 коду (оба поля должны совпадать)
            if existing.get("callsign") == aeroplane_data.get(
                "callsign"
            ) and existing.get("icao24") == aeroplane_data.get("icao24"):
                return True
        return False

    def add_aeroplane(self, aeroplane_data: Dict[str, Any]) -> bool:
        """
        Добавление информации о самолете в JSON-файл.
        Не сохраняет дубликаты.

        Args:
            aeroplane_data: Словарь с данными о самолете

        Returns:
            bool: True если добавление успешно, иначе False
        """
        try:
            data = self._load_data()

            if self._is_duplicate(aeroplane_data, data):
                logger.info(
                    f"⚠️ Самолет {aeroplane_data.get('callsign')} уже существует в файле"
                )
                return False

            data.append(aeroplane_data)
            self._save_data(data)
            logger.info(f"✅ Добавлен самолет {aeroplane_data.get('callsign')}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка при добавлении самолета: {e}")
            return False

    def get_aeroplanes(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получение данных о самолетах из JSON-файла по критериям.

        Args:
            **criteria: Критерии фильтрации:
                - origin_country: страна регистрации
                - altitude_min: минимальная высота
                - altitude_max: максимальная высота
                - velocity_min: минимальная скорость
                - on_ground: на земле (True/False)
                - callsign: позывной

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список самолетов
        """
        data = self._load_data()

        if not criteria:
            logger.info(f"📖 Загружено {len(data)} записей без фильтрации")
            return data

        result = []
        for aeroplane in data:
            match = True

            for key, value in criteria.items():
                if key == "altitude_min":
                    if aeroplane.get("altitude", 0) < value:
                        match = False
                        break
                elif key == "altitude_max":
                    if aeroplane.get("altitude", 0) > value:
                        match = False
                        break
                elif key == "velocity_min":
                    if aeroplane.get("velocity", 0) < value:
                        match = False
                        break
                elif key == "on_ground":
                    if aeroplane.get("on_ground") != value:
                        match = False
                        break
                else:
                    if aeroplane.get(key) != value:
                        match = False
                        break

            if match:
                result.append(aeroplane)

        logger.info(f"🔍 Найдено {len(result)} записей по критериям {criteria}")
        return result

    def delete_aeroplane(self, aeroplane_data: Dict[str, Any]) -> bool:
        """
        Удаление информации о самолете из JSON-файла.

        Args:
            aeroplane_data: Словарь с данными о самолете для удаления

        Returns:
            bool: True если удаление успешно, иначе False
        """
        try:
            data = self._load_data()
            original_length = len(data)

            # Удаляем по совпадению callsign и icao24
            data = [
                item
                for item in data
                if not (
                    item.get("callsign") == aeroplane_data.get("callsign")
                    and item.get("icao24") == aeroplane_data.get("icao24")
                )
            ]

            if len(data) < original_length:
                self._save_data(data)
                logger.info(f"🗑️ Удален самолет {aeroplane_data.get('callsign')}")
                return True

            logger.info(f"⚠️ Самолет {aeroplane_data.get('callsign')} не найден")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка при удалении самолета: {e}")
            return False

    def get_all_countries(self) -> List[str]:
        """
        Получение списка всех стран, для которых есть данные в файле.

        Returns:
            List[str]: Список уникальных стран
        """
        data = self._load_data()
        countries = list(set(item.get("origin_country", "Unknown") for item in data))
        logger.info(f"🌍 Найдено стран в файле: {len(countries)}")
        return countries

    def get_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики по сохраненным данным.

        Returns:
            Dict[str, Any]: Словарь со статистикой
        """
        data = self._load_data()
        if not data:
            return {"total": 0, "countries": [], "avg_altitude": 0, "avg_velocity": 0}

        altitudes = [a.get("altitude", 0) for a in data]
        velocities = [a.get("velocity", 0) for a in data]
        countries = list(set(a.get("origin_country", "Unknown") for a in data))

        return {
            "total": len(data),
            "countries": countries,
            "avg_altitude": sum(altitudes) / len(altitudes),
            "avg_velocity": sum(velocities) / len(velocities),
            "on_ground_count": sum(1 for a in data if a.get("on_ground", False)),
            "in_air_count": sum(1 for a in data if not a.get("on_ground", True)),
        }
