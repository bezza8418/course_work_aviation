"""
Модуль с классом Aeroplane для представления информации о самолете.
Содержит валидацию данных, методы сравнения и преобразования.
"""

from typing import Any, Dict, List, Optional


class Aeroplane:
    """
    Класс для представления информации о самолете.

    Использует __slots__ для экономии памяти.
    Поддерживает сравнение самолетов по высоте полета.

    Атрибуты:
        callsign: Позывной самолета
        origin_country: Страна регистрации
        velocity: Скорость полета (м/с)
        altitude: Высота полета (м)
        icao24: Уникальный идентификатор транспондера
        longitude: Долгота
        latitude: Широта
        on_ground: Находится ли на земле
        true_track: Курс
        vertical_rate: Вертикальная скорость
        geo_altitude: Геодезическая высота
    """

    __slots__ = (
        "_callsign",
        "_origin_country",
        "_velocity",
        "_altitude",
        "_icao24",
        "_longitude",
        "_latitude",
        "_on_ground",
        "_true_track",
        "_vertical_rate",
        "_geo_altitude",
    )

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        altitude: float,
        **kwargs: Any,
    ) -> None:
        """
        Инициализация объекта самолета.

        Args:
            callsign: Позывной самолета
            origin_country: Страна регистрации
            velocity: Скорость полета (м/с)
            altitude: Высота полета (м)
            **kwargs: Дополнительные параметры (icao24, координаты и т.д.)
        """
        self._callsign = self._validate_string(callsign)
        self._origin_country = self._validate_string(origin_country)
        self._velocity = self._validate_velocity(velocity)
        self._altitude = self._validate_altitude(altitude)
        self._icao24 = self._validate_string(kwargs.get("icao24", ""))
        self._longitude = self._validate_float(kwargs.get("longitude"))
        self._latitude = self._validate_float(kwargs.get("latitude"))
        self._on_ground = kwargs.get("on_ground", True)
        self._true_track = kwargs.get("true_track")
        self._vertical_rate = kwargs.get("vertical_rate")
        self._geo_altitude = self._validate_altitude(kwargs.get("geo_altitude", 0))

    # ==================== Приватные методы валидации ====================

    @staticmethod
    def _validate_string(value: Any) -> str:
        """
        Приватный метод валидации строковых значений.

        Args:
            value: Проверяемое значение

        Returns:
            str: Валидная строка или значение по умолчанию
        """
        if not value or not isinstance(value, str):
            return "Unknown"
        return value.strip()  # type: ignore[no-any-return]

    @staticmethod
    def _validate_velocity(value: Any) -> float:
        """
        Приватный метод валидации скорости (должна быть >= 0).

        Args:
            value: Проверяемое значение

        Returns:
            float: Валидная скорость (неотрицательная)
        """
        try:
            val = float(value)
            if val < 0:
                return 0.0
            return val
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _validate_altitude(value: Any) -> float:
        """
        Приватный метод валидации высоты.

        Args:
            value: Проверяемое значение

        Returns:
            float: Валидная высота
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _validate_float(value: Any) -> Optional[float]:
        """
        Приватный метод валидации чисел с плавающей точкой.

        Args:
            value: Проверяемое значение

        Returns:
            Optional[float]: Валидное число или None
        """
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    # ==================== Геттеры (свойства) ====================

    @property
    def callsign(self) -> str:
        """Позывной самолета."""
        return self._callsign

    @property
    def origin_country(self) -> str:
        """Страна регистрации самолета."""
        return self._origin_country

    @property
    def velocity(self) -> float:
        """Скорость полета (м/с)."""
        return self._velocity

    @property
    def altitude(self) -> float:
        """Высота полета (м)."""
        return self._altitude

    @property
    def icao24(self) -> str:
        """Уникальный идентификатор транспондера (ICAO24)."""
        return self._icao24

    @property
    def longitude(self) -> Optional[float]:
        """Долгота."""
        return self._longitude

    @property
    def latitude(self) -> Optional[float]:
        """Широта."""
        return self._latitude

    @property
    def on_ground(self) -> bool:
        """Находится ли самолет на земле."""
        return self._on_ground

    # ==================== Магические методы сравнения ====================

    def __eq__(self, other: object) -> bool:
        """Сравнение по высоте: равенство."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude == other.altitude

    def __ne__(self, other: object) -> bool:
        """Сравнение по высоте: неравенство."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude != other.altitude  # type: ignore[no-any-return]

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте: меньше."""
        return self.altitude < other.altitude

    def __le__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте: меньше или равно."""
        return self.altitude <= other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте: больше."""
        return self.altitude > other.altitude

    def __ge__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте: больше или равно."""
        return self.altitude >= other.altitude

    # ==================== Методы преобразования ====================

    def __repr__(self) -> str:
        """Строковое представление объекта."""
        return (
            f"Aeroplane(callsign='{self.callsign}', "
            f"origin_country='{self.origin_country}', "
            f"velocity={self.velocity}, altitude={self.altitude})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта в словарь для сохранения в JSON.

        Returns:
            Dict[str, Any]: Словарь с данными самолета
        """
        return {
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
            "icao24": self.icao24,
            "longitude": self._longitude,
            "latitude": self._latitude,
            "on_ground": self._on_ground,
            "true_track": self._true_track,
            "vertical_rate": self._vertical_rate,
            "geo_altitude": self._geo_altitude,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Aeroplane":
        """
        Создание объекта Aeroplane из словаря.

        Args:
            data: Словарь с данными самолета

        Returns:
            Aeroplane: Объект самолета
        """
        return cls(
            callsign=data.get("callsign", "N/A"),
            origin_country=data.get("origin_country", "Unknown"),
            velocity=data.get("velocity", 0),
            altitude=data.get("altitude", 0),
            icao24=data.get("icao24", ""),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            on_ground=data.get("on_ground", True),
            true_track=data.get("true_track"),
            vertical_rate=data.get("vertical_rate"),
            geo_altitude=data.get("geo_altitude", 0),
        )

    @classmethod
    def cast_to_object_list(cls, data_list: List[Dict[str, Any]]) -> List["Aeroplane"]:
        """
        Преобразование списка словарей в список объектов Aeroplane.

        Args:
            data_list: Список словарей с данными о самолетах

        Returns:
            List[Aeroplane]: Список объектов самолетов
        """
        return [cls.from_dict(data) for data in data_list]
