"""
Тесты для абстрактных классов.
"""

import pytest

from src.abstract_classes import BaseAPI, BaseFileStorage


class TestAbstractClasses:
    """Тесты для абстрактных классов."""

    def test_baseapi_cannot_instantiate(self):
        """Тест: невозможно создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError):
            BaseAPI("https://example.com")

    def test_basefilestorage_cannot_instantiate(self):
        """Тест: невозможно создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError):
            BaseFileStorage()
