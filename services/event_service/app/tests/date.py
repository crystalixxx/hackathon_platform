from datetime import datetime, timezone

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from services.event_service.app.database.schemas.date import DateSchema


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.team = AsyncMock()
    uow.team_user = AsyncMock()
    uow.users = AsyncMock()
    return uow


def test_date_basic():
    data = {"date_start": "01.01.2025", "date_end": "01.01.2026"}

    assert