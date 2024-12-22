import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.request import RequestService
from app.database.schemas.request import RequestCreate


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.request = AsyncMock()
    return uow


@pytest.fixture
def request_service():
    return RequestService()


@pytest.mark.asyncio
async def test_create_request(mock_uow, request_service):
    request_data = RequestCreate(user_id=1, request_team_id=2, sent_by_team=True)
    mock_uow.request.add_one.return_value = {"id": 1, **request_data.model_dump()}

    result = await request_service.create_request(mock_uow, request_data)

    assert result["id"] == 1
    mock_uow.request.add_one.assert_called_once_with(request_data.model_dump(exclude_none=True))


@pytest.mark.asyncio
async def test_get_request_by_id_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = {"id": request_id, "user_id": 1}

    result = await request_service.get_request_by_id(mock_uow, request_id)

    assert result["id"] == request_id
    mock_uow.request.find_one.assert_called_once_with({"id": request_id})


@pytest.mark.asyncio
async def test_get_request_by_id_not_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = None

    result = await request_service.get_request_by_id(mock_uow, request_id)

    assert result is None


@pytest.mark.asyncio
async def test_get_requests_of_user(mock_uow, request_service):
    user_id = 1

    mock_uow.request.find_some.return_value = [
        {"id": 1, "user_id": user_id},
        {"id": 2, "user_id": user_id},
    ]

    result = await request_service.get_requests_of_user(mock_uow, user_id)

    assert len(result) == 2
    assert result[0]["user_id"] == user_id
    mock_uow.request.find_some.assert_called_once_with({"user_id": user_id})


@pytest.mark.asyncio
async def test_get_requests_of_team(mock_uow, request_service):
    team_id = 2

    mock_uow.request.find_some.return_value = [
        {"id": 1, "request_team_id": team_id},
        {"id": 2, "request_team_id": team_id},
    ]

    result = await request_service.get_requests_of_team(mock_uow, team_id)

    assert len(result) == 2
    assert result[0]["request_team_id"] == team_id
    mock_uow.request.find_some.assert_called_once_with({"request_team_id": team_id})


@pytest.mark.asyncio
async def test_delete_request_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = {"id": request_id}
    mock_uow.request.delete.return_value = {"id": request_id}

    result = await request_service.delete_request(mock_uow, request_id)

    assert result["id"] == request_id
    mock_uow.request.delete.assert_called_once_with({"id": request_id})


@pytest.mark.asyncio
async def test_delete_request_not_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await request_service.delete_request(mock_uow, request_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Реквест #{request_id} не найден."


@pytest.mark.asyncio
async def test_approve_request_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = {"id": request_id, "is_ok": False}
    mock_uow.request.update.return_value = {"id": request_id, "is_ok": True}

    result = await request_service.approve_request(mock_uow, request_id)

    assert result["is_ok"] is True
    mock_uow.request.update.assert_called_once_with({"id": request_id}, {"is_ok": True})


@pytest.mark.asyncio
async def test_approve_request_not_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await request_service.approve_request(mock_uow, request_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Реквест #{request_id} не найден."


@pytest.mark.asyncio
async def test_reject_request_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = {"id": request_id}
    mock_uow.request.delete.return_value = {"id": request_id}

    result = await request_service.reject_request(mock_uow, request_id)

    assert result["id"] == request_id
    mock_uow.request.delete.assert_called_once_with({"id": request_id})


@pytest.mark.asyncio
async def test_reject_request_not_found(mock_uow, request_service):
    request_id = 1
    mock_uow.request.find_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await request_service.reject_request(mock_uow, request_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Реквест #{request_id} не найден."


@pytest.mark.asyncio
async def test_get_requests_sent_by_team(mock_uow, request_service):
    team_id = 2

    mock_uow.request.find_some.return_value = [
        {"id": 1, "request_team_id": team_id, "sent_by_team": True},
        {"id": 2, "request_team_id": team_id, "sent_by_team": True},
    ]

    result = await request_service.get_requests_sent_by_team(mock_uow, team_id)

    assert len(result) == 2
    assert all(r["sent_by_team"] is True for r in result)

    mock_uow.request.find_some.assert_called_once_with(
        {"request_team_id": team_id, "sent_by_team": True}
    )


@pytest.mark.asyncio
async def test_get_requests_to_team(mock_uow, request_service):
    team_id = 2

    mock_uow.request.find_some.return_value = [
        {"id": 1, "request_team_id": team_id, "sent_by_team": False},
        {"id": 2, "request_team_id": team_id, "sent_by_team": False},
    ]

    result = await request_service.get_requests_to_team(mock_uow, team_id)

    assert len(result) == 2
    assert all(r["sent_by_team"] is False for r in result)

    mock_uow.request.find_some.assert_called_once_with(
        {"request_team_id": team_id, "sent_by_team": False}
    )
