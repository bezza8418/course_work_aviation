"""
Тесты для классов работы с файлами (JSONStorage).
"""

import json
import os

import pytest
from src.file_classes import JSONStorage


class TestJSONStorage:
    """Тесты JSONStorage."""

    def test_init_creates_file(self, temp_json_file):
        """Тест: при инициализации создается файл."""
        storage = JSONStorage(str(temp_json_file))
        assert os.path.exists(temp_json_file)

    def test_add_aeroplane(self, temp_json_file, sample_aeroplane_dict):
        """Тест добавления самолета в файл."""
        storage = JSONStorage(str(temp_json_file))
        result = storage.add_aeroplane(sample_aeroplane_dict)
        assert result is True

        data = storage.get_aeroplanes()
        assert len(data) == 1
        assert data[0]["callsign"] == "TEST456"

    def test_add_duplicate_aeroplane(self, temp_json_file, sample_aeroplane_dict):
        """Тест: дубликаты не добавляются."""
        storage = JSONStorage(str(temp_json_file))
        storage.add_aeroplane(sample_aeroplane_dict)
        result = storage.add_aeroplane(sample_aeroplane_dict)

        assert result is False
        data = storage.get_aeroplanes()
        assert len(data) == 1

    def test_get_aeroplanes_filter_by_country(self, temp_json_file, sample_aeroplane_dict):
        """Тест фильтрации по стране."""
        storage = JSONStorage(str(temp_json_file))
        storage.add_aeroplane(sample_aeroplane_dict)

        # Добавим еще один самолет из другой страны
        another = {"callsign": "ANOTHER", "origin_country": "Germany", "velocity": 200, "altitude": 8000}
        storage.add_aeroplane(another)

        filtered = storage.get_aeroplanes(origin_country="France")
        assert len(filtered) == 1
        assert filtered[0]["callsign"] == "TEST456"

    def test_get_aeroplanes_filter_by_altitude_range(self, temp_json_file):
        """Тест фильтрации по диапазону высот."""
        storage = JSONStorage(str(temp_json_file))
        storage.add_aeroplane({"callsign": "LOW", "origin_country": "USA", "velocity": 200, "altitude": 3000})
        storage.add_aeroplane({"callsign": "MED", "origin_country": "USA", "velocity": 250, "altitude": 8000})
        storage.add_aeroplane({"callsign": "HIGH", "origin_country": "USA", "velocity": 300, "altitude": 12000})

        filtered = storage.get_aeroplanes(altitude_min=5000, altitude_max=10000)
        assert len(filtered) == 1
        assert filtered[0]["callsign"] == "MED"

    def test_delete_aeroplane(self, temp_json_file, sample_aeroplane_dict):
        """Тест удаления самолета."""
        storage = JSONStorage(str(temp_json_file))
        storage.add_aeroplane(sample_aeroplane_dict)
        assert len(storage.get_aeroplanes()) == 1

        result = storage.delete_aeroplane(sample_aeroplane_dict)
        assert result is True
        assert len(storage.get_aeroplanes()) == 0

    def test_delete_nonexistent_aeroplane(self, temp_json_file, sample_aeroplane_dict):
        """Тест удаления несуществующего самолета."""
        storage = JSONStorage(str(temp_json_file))
        result = storage.delete_aeroplane(sample_aeroplane_dict)
        assert result is False

    def test_get_statistics(self, temp_json_file):
        """Тест получения статистики."""
        storage = JSONStorage(str(temp_json_file))
        storage.add_aeroplane({"callsign": "A1", "origin_country": "Russia", "velocity": 250, "altitude": 10000, "on_ground": False})
        storage.add_aeroplane({"callsign": "A2", "origin_country": "USA", "velocity": 300, "altitude": 12000, "on_ground": False})
        storage.add_aeroplane({"callsign": "A3", "origin_country": "Russia", "velocity": 0, "altitude": 0, "on_ground": True})

        stats = storage.get_statistics()
        assert stats["total"] == 3
        assert len(stats["countries"]) == 2
        assert stats["on_ground_count"] == 1
        assert stats["in_air_count"] == 2
