import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.team = AsyncMock()
    uow.team_user = AsyncMock()
    uow.users = AsyncMock()
    return uow

