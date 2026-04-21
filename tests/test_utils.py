"""
Тесты для вспомогательных функций из модуля utils.
"""

import pytest
from src.aeroplane import Aeroplane
from src.utils import (
    filter_by_altitude_range,
    filter_by_country,
    filter_by_velocity_range,
    get_top_n_aeroplanes,
    parse_altitude_range,
    print_aeroplanes,
    sort_aeroplanes_by_altitude,
    sort_aeroplanes_by_velocity,
)


class TestUtils:
    """Тесты вспомогательных функций."""

    def test_sort_by_altitude_desc(self, sample_aeroplanes_list):
        """Тест сортировки по высоте (по убыванию)."""
        sorted_list = sort_aeroplanes_by_altitude(sample_aeroplanes_list, reverse=True)
        assert sorted_list[0].altitude == 12000.0
        assert sorted_list[1].altitude == 10000.0
        assert sorted_list[2].altitude == 8000.0
        assert sorted_list[3].altitude == 5000.0

    def test_sort_by_altitude_asc(self, sample_aeroplanes_list):
        """Тест сортировки по высоте (по возрастанию)."""
        sorted_list = sort_aeroplanes_by_altitude(sample_aeroplanes_list, reverse=False)
        assert sorted_list[0].altitude == 5000.0
        assert sorted_list[1].altitude == 8000.0
        assert sorted_list[2].altitude == 10000.0
        assert sorted_list[3].altitude == 12000.0

    def test_sort_by_velocity_desc(self, sample_aeroplanes_list):
        """Тест сортировки по скорости (по убыванию)."""
        sorted_list = sort_aeroplanes_by_velocity(sample_aeroplanes_list, reverse=True)
        assert sorted_list[0].velocity == 300.0
        assert sorted_list[1].velocity == 250.0
        assert sorted_list[2].velocity == 200.0
        assert sorted_list[3].velocity == 150.0

    def test_get_top_n(self, sample_aeroplanes_list):
        """Тест получения топ N самолетов."""
        sorted_list = sort_aeroplanes_by_altitude(sample_aeroplanes_list)
        top_2 = get_top_n_aeroplanes(sorted_list, 2)
        assert len(top_2) == 2
        assert top_2[0].altitude == 12000.0

    def test_filter_by_country(self, sample_aeroplanes_list):
        """Тест фильтрации по стране."""
        filtered = filter_by_country(sample_aeroplanes_list, ["Russia"])
        assert len(filtered) == 2
        for a in filtered:
            assert a.origin_country == "Russia"

    def test_filter_by_country_empty(self, sample_aeroplanes_list):
        """Тест фильтрации с пустым списком стран."""
        filtered = filter_by_country(sample_aeroplanes_list, [])
        assert len(filtered) == len(sample_aeroplanes_list)

    def test_filter_by_altitude_range(self, sample_aeroplanes_list):
        """Тест фильтрации по диапазону высот."""
        filtered = filter_by_altitude_range(sample_aeroplanes_list, min_altitude=9000, max_altitude=13000)
        assert len(filtered) == 2
        assert all(9000 <= a.altitude <= 13000 for a in filtered)

    def test_filter_by_altitude_range_min_only(self, sample_aeroplanes_list):
        """Тест фильтрации только по минимальной высоте."""
        filtered = filter_by_altitude_range(sample_aeroplanes_list, min_altitude=9000)
        assert len(filtered) == 2

    def test_filter_by_velocity_range(self, sample_aeroplanes_list):
        """Тест фильтрации по диапазону скоростей."""
        filtered = filter_by_velocity_range(sample_aeroplanes_list, min_velocity=200, max_velocity=280)
        assert len(filtered) == 2

    def test_parse_altitude_range_with_dash(self):
        """Тест парсинга диапазона высот (формат с дефисом)."""
        min_alt, max_alt = parse_altitude_range("1000-5000")
        assert min_alt == 1000.0
        assert max_alt == 5000.0

    def test_parse_altitude_range_single_value(self):
        """Тест парсинга диапазона высот (одиночное значение)."""
        min_alt, max_alt = parse_altitude_range("10000")
        assert min_alt is None
        assert max_alt == 10000.0

    def test_parse_altitude_range_empty(self):
        """Тест парсинга пустой строки."""
        min_alt, max_alt = parse_altitude_range("")
        assert min_alt is None
        assert max_alt is None
