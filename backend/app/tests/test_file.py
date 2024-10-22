from pydantic import ValidationError
import pytest
from ..database.schemas import TagCreate


def test_tag_create():
    """Создает тег"""
    tag = TagCreate(color="#FF0000", name="Test Tag")
    assert tag.color == "#FF0000"
    assert tag.name == "Test Tag"


def test_tag_create_rgba():
    """Проверяет создание тега с цветом палитры rgba"""
    tag = TagCreate(color="rgba(255, 87, 51, 0.5)", transparency=0.5, name="Test Tag")
    assert tag.color == "rgba(255, 87, 51, 0.5)"
    assert tag.transparency == 0.5
