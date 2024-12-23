import pytest
from pydantic import ValidationError

from services.event_service.app.database.schemas.location import LocationBase


def test_location_base_invalid_empty_title():
    data = {"title": ""}

    with pytest.raises(ValidationError):
        LocationBase(**data)
