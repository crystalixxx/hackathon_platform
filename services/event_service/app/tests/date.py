from datetime import datetime, timezone

from services.event_service.app.database.schemas.date import DateSchema


def test_date_basic():
    data = {"date_start": "01.01.2025", "date_end": "01.01.2026"}

    date_start = data["date_start"]
    date_end = data["date_end"]

    assert date_start == data["date_start"]
    assert date_end == data["date_end"]


def test_date_schema_creation():
    data = {
        "id": 1,
        "date_start": "2025-01-01T00:00:00",
        "date_end": "2026-01-01T00:00:00",
    }

    date_instance = DateSchema(
        id=data["id"],
        date_start=datetime.fromisoformat(data["date_start"]),
        date_end=datetime.fromisoformat(data["date_end"]),
    )

    assert date_instance.id == 1
    assert date_instance.date_start == datetime.fromisoformat(data["date_start"])
    assert date_instance.date_end == datetime.fromisoformat(data["date_end"])
