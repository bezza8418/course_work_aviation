"""
Модуль с классом CSVStorage для работы с CSV-файлами.
Реализует сохранение данных о самолетах в CSV формате.
"""

import csv
import logging
import os
from typing import Any, Dict, List

from src.abstract_classes import BaseFileStorage

logger = logging.getLogger(__name__)


class CSVStorage(BaseFileStorage):
    """
    Класс для работы с CSV-файлом как хранилищем данных о самолетах.
    Реализует добавление данных (основной метод).
    """

    def __init__(self, filename: str = "data/aeroplanes.csv") -> None:
        """
        Инициализация CSV хранилища.

        Args:
            filename: Имя файла для хранения данных
        """
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создает директорию и файл с заголовками, если не существуют."""
        directory = os.path.dirname(self._filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self._filename):
            with open(self._filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "callsign",
                        "origin_country",
                        "velocity",
                        "altitude",
                        "icao24",
                        "longitude",
                        "latitude",
                        "on_ground",
                    ]
                )
            logger.info(f"Создан CSV файл: {self._filename}")

    def add_aeroplane(self, aeroplane_data: Dict[str, Any]) -> bool:
        """
        Добавление информации о самолете в CSV-файл.

        Args:
            aeroplane_data: Словарь с данными о самолете

        Returns:
            bool: True если добавление успешно, иначе False
        """
        try:
            with open(self._filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        aeroplane_data.get("callsign", ""),
                        aeroplane_data.get("origin_country", ""),
                        aeroplane_data.get("velocity", 0),
                        aeroplane_data.get("altitude", 0),
                        aeroplane_data.get("icao24", ""),
                        aeroplane_data.get("longitude", ""),
                        aeroplane_data.get("latitude", ""),
                        aeroplane_data.get("on_ground", True),
                    ]
                )
            logger.info(f"Добавлен самолет {aeroplane_data.get('callsign')} в CSV")
            return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении в CSV: {e}")
            return False

    def get_aeroplanes(self, **criteria: Any) -> List[Dict[str, Any]]:
        """
        Получение данных о самолетах из CSV-файла (заглушка).

        Args:
            **criteria: Критерии фильтрации

        Returns:
            List[Dict[str, Any]]: Пустой список (заглушка)
        """
        logger.warning("Метод get_aeroplanes для CSV временно не реализован")
        return []

    def delete_aeroplane(self, aeroplane_data: Dict[str, Any]) -> bool:
        """
        Удаление информации о самолете из CSV-файла (заглушка).

        Args:
            aeroplane_data: Словарь с данными о самолете

        Returns:
            bool: False (заглушка)
        """
        logger.warning("Метод delete_aeroplane для CSV временно не реализован")
        return False
