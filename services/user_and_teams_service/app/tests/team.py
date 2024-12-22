import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.team import TeamService
from app.database.schemas.team import TeamCreate, TeamUpdate


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.team = AsyncMock()
    uow.team_user = AsyncMock()
    uow.users = AsyncMock()
    return uow


@pytest.fixture
def team_service():
    return TeamService()


@pytest.mark.asyncio
async def test_create_team(mock_uow, team_service):
    team_data = TeamCreate(title="Test Team", captain_id=1)
    mock_uow.team.add_one.return_value = {"id": 1, "title": "Test Team", "captain_id": 1}

    result = await team_service.create_team(mock_uow, team_data)

    assert result["title"] == "Test Team"
    mock_uow.team.add_one.assert_called_once()


@pytest.mark.asyncio
async def test_get_team_by_id_found(mock_uow, team_service):
    team_id = 1
    mock_uow.team.find_one.return_value = {"id": team_id, "title": "Test Team"}

    result = await team_service.get_team_by_id(mock_uow, team_id)

    assert result["id"] == team_id
    mock_uow.team.find_one.assert_called_once_with({"id": team_id})


@pytest.mark.asyncio
async def test_get_team_by_id_not_found(mock_uow, team_service):
    team_id = 1
    mock_uow.team.find_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await team_service.get_team_by_id(mock_uow, team_id)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_team(mock_uow, team_service):
    team_id = 1
    team_update = TeamUpdate(title="Updated Team")
    mock_uow.team.find_one.return_value = {"id": team_id, "title": "Test Team"}
    mock_uow.team.update.return_value = {"id": team_id, "title": "Updated Team"}

    result = await team_service.update_team(mock_uow, team_update, team_id)

    assert result["title"] == "Updated Team"
    mock_uow.team.update.assert_called_once_with({"id": team_id}, team_update.model_dump(exclude_unset=True))


@pytest.mark.asyncio
async def test_delete_team(mock_uow, team_service):
    team_id = 1
    mock_uow.team.find_one.return_value = {"id": team_id, "title": "Test Team"}
    mock_uow.team.delete.return_value = {"id": team_id, "title": "Test Team"}

    result = await team_service.delete_team(mock_uow, team_id)

    assert result["id"] == team_id
    mock_uow.team.delete.assert_called_once_with({"id": team_id})


@pytest.mark.asyncio
async def test_add_member(mock_uow, team_service):
    team_id = 1
    user_id = 1
    mock_uow.team.find_one.return_value = {"id": team_id, "title": "Test Team"}
    mock_uow.users.find_one.return_value = {"id": user_id, "name": "Test User"}
    mock_uow.team_user.find_one.return_value = None
    mock_uow.team_user.add_one.return_value = {"team_id": team_id, "user_id": user_id}

    result = await team_service.add_member(mock_uow, team_id, user_id)

    assert result["user_id"] == user_id
    mock_uow.team_user.add_one.assert_called_once()


@pytest.mark.asyncio
async def test_remove_member(mock_uow, team_service):
    team_id = 1
    user_id = 1
    mock_uow.team.find_one.return_value = {"id": team_id, "title": "Test Team", "captain_id": 2}
    mock_uow.team_user.find_one.return_value = {"team_id": team_id, "user_id": user_id}
    mock_uow.team_user.delete.return_value = {"team_id": team_id, "user_id": user_id}

    result = await team_service.remove_member(mock_uow, team_id, user_id)

    assert result["user_id"] == user_id
    mock_uow.team_user.delete.assert_called_once_with({"team_id": team_id, "user_id": user_id})


@pytest.mark.asyncio
async def test_is_member_of_team(mock_uow, team_service):
    team_id = 1
    user_id = 1
    mock_uow.team_user.find_one.return_value = {"team_id": team_id, "user_id": user_id}

    result = await team_service.is_member_of_team(mock_uow, team_id, user_id)

    assert result is True


@pytest.mark.asyncio
async def test_change_captain(mock_uow, team_service):
    team_id = 1
    user_id = 2
    mock_uow.team.find_one.return_value = {"id": team_id, "title": "Test Team", "captain_id": 1}
    mock_uow.team_user.find_some.return_value = [{"id": user_id, "user_id": user_id}]
    mock_uow.team.update.return_value = {"id": team_id, "title": "Test Team", "captain_id": user_id}

    result = await team_service.change_captain(mock_uow, team_id, user_id)

    assert result["captain_id"] == user_id
