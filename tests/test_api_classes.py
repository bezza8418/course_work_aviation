"""
Тесты для классов работы с API (AviationAPI).
"""

import pytest
from unittest.mock import Mock, patch
from src.api_classes import AviationAPI


class TestAviationAPI:
    """Тесты для AviationAPI."""

    @patch('src.api_classes.requests.get')
    def test_connect_success(self, mock_get):
        """Тест успешного подключения к API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = AviationAPI()
        result = api._connect()

        assert result is True
        assert api._connected is True

    @patch('src.api_classes.requests.get')
    def test_connect_failure(self, mock_get):
        """Тест ошибки подключения к API."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = AviationAPI()
        result = api._connect()

        assert result is False
        assert api._connected is False

    @patch('src.api_classes.requests.get')
    def test_get_country_bounding_box_success(self, mock_get):
        """Тест успешного получения bounding box страны."""
        # Мокаем ответ от Nominatim
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"boundingbox": ["55.0", "82.0", "19.0", "180.0"]}
        ]
        mock_get.return_value = mock_response

        api = AviationAPI()
        api._connected = True
        result = api.get_country_bounding_box("Russia")

        assert result == [55.0, 82.0, 19.0, 180.0]

    @patch('src.api_classes.requests.get')
    def test_get_country_bounding_box_not_found(self, mock_get):
        """Тест: страна не найдена."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        api = AviationAPI()
        api._connected = True
        result = api.get_country_bounding_box("NonExistentCountry")

        assert result is None

    @patch('src.api_classes.requests.get')
    def test_get_aeroplanes_success(self, mock_get):
        """Тест успешного получения данных о самолетах."""
        # Мокаем bounding box
        mock_bbox_response = Mock()
        mock_bbox_response.status_code = 200
        mock_bbox_response.json.return_value = [
            {"boundingbox": ["55.0", "82.0", "19.0", "180.0"]}
        ]

        # Мокаем ответ OpenSky
        mock_opensky_response = Mock()
        mock_opensky_response.status_code = 200
        mock_opensky_response.json.return_value = {
            "states": [
                ["abc123", "FL123", "Russia", 123456, 123457, 37.6, 55.7, 10500, False, 250.5, 180, 5, None, 10550, "1234", False, 0],
                ["def456", "FL456", "USA", 123458, 123459, 10.0, 50.0, 12000, False, 300.0, 90, 3, None, 12050, "5678", False, 0],
            ]
        }

        mock_get.side_effect = [mock_bbox_response, mock_opensky_response]

        api = AviationAPI()
        api._connected = True
        result = api.get_aeroplanes("Russia")

        assert len(result) == 2
        assert result[0]["callsign"] == "FL123"
        assert result[0]["origin_country"] == "Russia"
        assert result[1]["callsign"] == "FL456"

    @patch('src.api_classes.requests.get')
    def test_get_aeroplanes_no_bounding_box(self, mock_get):
        """Тест: bounding box не найден."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        api = AviationAPI()
        api._connected = True
        result = api.get_aeroplanes("NonExistentCountry")

        assert result == []

    @patch('src.api_classes.requests.get')
    def test_get_aeroplanes_empty_result(self, mock_get):
        """Тест: самолеты не найдены."""
        # Мокаем bounding box
        mock_bbox_response = Mock()
        mock_bbox_response.status_code = 200
        mock_bbox_response.json.return_value = [
            {"boundingbox": ["55.0", "82.0", "19.0", "180.0"]}
        ]

        # Мокаем ответ OpenSky (пустой)
        mock_opensky_response = Mock()
        mock_opensky_response.status_code = 200
        mock_opensky_response.json.return_value = {"states": []}

        mock_get.side_effect = [mock_bbox_response, mock_opensky_response]

        api = AviationAPI()
        api._connected = True
        result = api.get_aeroplanes("Russia")

        assert result == []

    @patch('src.api_classes.requests.get')
    def test_get_aeroplanes_api_error(self, mock_get):
        """Тест: ошибка OpenSky API."""
        # Мокаем bounding box
        mock_bbox_response = Mock()
        mock_bbox_response.status_code = 200
        mock_bbox_response.json.return_value = [
            {"boundingbox": ["55.0", "82.0", "19.0", "180.0"]}
        ]

        # Мокаем ошибку OpenSky
        mock_opensky_response = Mock()
        mock_opensky_response.status_code = 500

        mock_get.side_effect = [mock_bbox_response, mock_opensky_response]

        api = AviationAPI()
        api._connected = True
        result = api.get_aeroplanes("Russia")

        assert result == []
