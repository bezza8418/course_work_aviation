"""
Фикстуры для тестирования проекта.
Содержит общие данные и объекты для использования в тестах.
"""

import pytest
from src.aeroplane import Aeroplane


@pytest.fixture
def sample_aeroplane():
    """Фикстура: возвращает один тестовый самолет."""
    return Aeroplane(
        callsign="TEST123",
        origin_country="Russia",
        velocity=250.5,
        altitude=10500.0,
        icao24="123456",
        longitude=37.6176,
        latitude=55.7558,
        on_ground=False
    )


@pytest.fixture
def sample_aeroplanes_list():
    """Фикстура: возвращает список тестовых самолетов."""
    return [
        Aeroplane("FL123", "Russia", 250.0, 10000.0, icao24="AAA111"),
        Aeroplane("FL456", "USA", 300.0, 12000.0, icao24="BBB222"),
        Aeroplane("FL789", "Germany", 200.0, 8000.0, icao24="CCC333"),
        Aeroplane("FL000", "Russia", 150.0, 5000.0, icao24="DDD444", on_ground=True),
    ]


@pytest.fixture
def sample_aeroplane_dict():
    """Фикстура: возвращает словарь с данными самолета."""
    return {
        "callsign": "TEST456",
        "origin_country": "France",
        "velocity": 280.0,
        "altitude": 11000.0,
        "icao24": "654321",
        "longitude": 2.3522,
        "latitude": 48.8566,
        "on_ground": False,
        "true_track": 180.0,
        "vertical_rate": 5.0,
        "geo_altitude": 11050.0,
    }


@pytest.fixture
def temp_json_file(tmp_path):
    """Фикстура: возвращает временный JSON файл для тестов."""
    return tmp_path / "test_aeroplanes.json"
