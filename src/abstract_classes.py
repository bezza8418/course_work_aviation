"""
Модуль с абстрактными классами для работы с API.
Определяет интерфейсы для подключения к внешним сервисам.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAPI(ABC):
    """
    Абстрактный базовый класс для работы с внешними API.

    Этот класс определяет интерфейс, который должны реализовать
    все конкретные классы для работы с API сервисами.
    """

    def __init__(self, base_url: str) -> None:
        """
        Инициализация базового API класса.

        Args:
            base_url: Базовый URL API сервиса
        """
        self._base_url = base_url
        self._connected = False

    @abstractmethod
    def _connect(self) -> bool:
        """
        Приватный метод для установления соединения с API.

        Returns:
            bool: True если подключение успешно, иначе False
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах для указанной страны.

        Args:
            country: Название страны

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о самолетах
        """
        pass

    @abstractmethod
    def get_country_bounding_box(self, country: str) -> Optional[List[float]]:
        """
        Получение географических границ (bounding box) страны.

        Args:
            country: Название страны

        Returns:
            Optional[List[float]]: Список [юг, север, запад, восток] или None
        """
        pass


# ==================== Абстрактный класс для работы с файлами ====================


class BaseFileStorage(ABC):
    """
    Абстрактный базовый класс для работы с файловым хранилищем.
    Определяет интерфейс для добавления, получения и удаления данных.
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane_data: Dict[str, Any]) -> bool:
        """
        Добавление информации о самолете в файл.

        Args:
            aeroplane_data: Словарь с данными о самолете

        Returns:
            bool: True если добавление успешно, иначе False
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получение данных о самолетах из файла по указанным критериям.

        Args:
            **criteria: Критерии фильтрации (origin_country, altitude_min, altitude_max и т.д.)

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о самолетах
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane_data: Dict[str, Any]) -> bool:
        """
        Удаление информации о самолете из файла.

        Args:
            aeroplane_data: Словарь с данными о самолете для удаления

        Returns:
            bool: True если удаление успешно, иначе False
        """
        pass
