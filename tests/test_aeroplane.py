"""
Тесты для класса Aeroplane.
Проверяют создание объектов, валидацию и методы сравнения.
"""

import pytest
from src.aeroplane import Aeroplane


class TestAeroplane:
    """Тесты класса Aeroplane."""

    def test_aeroplane_creation(self, sample_aeroplane):
        """Тест создания объекта Aeroplane."""
        assert sample_aeroplane.callsign == "TEST123"
        assert sample_aeroplane.origin_country == "Russia"
        assert sample_aeroplane.velocity == 250.5
        assert sample_aeroplane.altitude == 10500.0
        assert sample_aeroplane.icao24 == "123456"

    def test_aeroplane_validation_invalid_string(self):
        """Тест валидации: некорректная строка."""
        a = Aeroplane("", "", 100, 5000)
        assert a.callsign == "Unknown"
        assert a.origin_country == "Unknown"

    def test_aeroplane_validation_negative_velocity(self):
        """Тест валидации: отрицательная скорость."""
        a = Aeroplane("FL123", "Russia", -100, 5000)
        assert a.velocity == 0.0

    def test_aeroplane_validation_invalid_velocity(self):
        """Тест валидации: некорректная скорость."""
        a = Aeroplane("FL123", "Russia", "invalid", 5000)
        assert a.velocity == 0.0

    def test_aeroplane_comparison_lt(self, sample_aeroplanes_list):
        """Тест сравнения: меньше."""
        assert sample_aeroplanes_list[2] < sample_aeroplanes_list[1]  # 8000 < 12000

    def test_aeroplane_comparison_gt(self, sample_aeroplanes_list):
        """Тест сравнения: больше."""
        assert sample_aeroplanes_list[1] > sample_aeroplanes_list[2]  # 12000 > 8000

    def test_aeroplane_comparison_eq(self):
        """Тест сравнения: равно."""
        a1 = Aeroplane("FL123", "Russia", 250, 10000)
        a2 = Aeroplane("FL456", "USA", 300, 10000)
        assert a1 == a2

    def test_aeroplane_to_dict(self, sample_aeroplane):
        """Тест преобразования в словарь."""
        data = sample_aeroplane.to_dict()
        assert data["callsign"] == "TEST123"
        assert data["origin_country"] == "Russia"
        assert data["velocity"] == 250.5
        assert data["altitude"] == 10500.0

    def test_aeroplane_from_dict(self, sample_aeroplane_dict):
        """Тест создания из словаря."""
        a = Aeroplane.from_dict(sample_aeroplane_dict)
        assert a.callsign == "TEST456"
        assert a.origin_country == "France"
        assert a.velocity == 280.0
        assert a.altitude == 11000.0

    def test_cast_to_object_list(self, sample_aeroplane_dict):
        """Тест преобразования списка словарей в список объектов."""
        data_list = [sample_aeroplane_dict, sample_aeroplane_dict]
        objects = Aeroplane.cast_to_object_list(data_list)
        assert len(objects) == 2
        assert isinstance(objects[0], Aeroplane)

    def test_repr(self, sample_aeroplane):
        """Тест строкового представления."""
        repr_str = repr(sample_aeroplane)
        assert "TEST123" in repr_str
        assert "Russia" in repr_str
