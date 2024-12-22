import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.user import UserService
from app.database.schemas.user import UserCreate, UserUpdate
from app.database.schemas.user_tag import UserTagCreate, UserTagUpdate


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.users = AsyncMock()
    uow.user_tags = AsyncMock()
    return uow


@pytest.fixture
def user_service():
    return UserService()


@pytest.mark.asyncio
async def test_create_user(mock_uow, user_service):
    user_data = UserCreate(email="test@example.com", password="password123")
    mock_uow.users.find_one.return_value = None
    mock_uow.users.add_one.return_value = 1

    user_id = await user_service.create_user(mock_uow, user_data)

    assert user_id == 1
    mock_uow.users.add_one.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_already_exists(mock_uow, user_service):
    user_data = UserCreate(email="test@example.com", password="password123")
    mock_uow.users.find_one.return_value = {"email": "test@example.com"}

    with pytest.raises(HTTPException) as exc_info:
        await user_service.create_user(mock_uow, user_data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "User with this email already exists"


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_uow, user_service):
    mock_uow.users.find_one.return_value = {
        "email": "test@example.com",
        "hashed_password": "$2b$12$hashedpasswordhere"
    }

    with pytest.mock.patch("app.core.security.verify_password", return_value=True):
        is_authenticated = await user_service.authenticate_user(
            mock_uow, "test@example.com", "password123"
        )

    assert is_authenticated is True


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(mock_uow, user_service):
    mock_uow.users.find_one.return_value = {
        "email": "test@example.com",
        "hashed_password": "$2b$12$hashedpasswordhere"
    }

    with pytest.mock.patch("app.core.security.verify_password", return_value=False):
        is_authenticated = await user_service.authenticate_user(
            mock_uow, "test@example.com", "wrongpassword"
        )

    assert is_authenticated is False


@pytest.mark.asyncio
async def test_update_user(mock_uow, user_service):
    user_id = 1
    user_update = UserUpdate(email="newemail@example.com")
    mock_uow.users.find_one.return_value = {"id": user_id, "email": "test@example.com"}
    mock_uow.users.update.return_value = {"id": user_id, "email": "newemail@example.com"}

    updated_user = await user_service.update_user(mock_uow, user_update, user_id)

    assert updated_user["email"] == "newemail@example.com"
    mock_uow.users.update.assert_called_once_with({"id": user_id}, user_update.model_dump(exclude_unset=True))


@pytest.mark.asyncio
async def test_update_user_not_found(mock_uow, user_service):
    user_id = 1
    user_update = UserUpdate(email="newemail@example.com")
    mock_uow.users.find_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await user_service.update_user(mock_uow, user_update, user_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User with this id does not exist"


@pytest.mark.asyncio
async def test_delete_user(mock_uow, user_service):
    user_id = 1
    mock_uow.users.find_one.return_value = {"id": user_id, "email": "test@example.com"}
    mock_uow.users.delete.return_value = {"id": user_id, "email": "test@example.com"}

    deleted_user = await user_service.delete_user(mock_uow, user_id)

    assert deleted_user["id"] == user_id
    mock_uow.users.delete.assert_called_once_with({"id": user_id})


@pytest.mark.asyncio
async def test_create_user_tag(mock_uow, user_service):
    user_id = 1
    tag_data = UserTagCreate(user_id=user_id, name="hawktuah")
    mock_uow.user_tags.find_one.return_value = None  # Тег с этим именем не существует
    mock_uow.user_tags.add_one.return_value = {"id": 1, "user_id": user_id, "name": "hawktuah"}

    created_tag = await user_service.create_user_tag(mock_uow, tag_data)

    assert created_tag["name"] == "hawktuah"
    mock_uow.user_tags.add_one.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_tag_already_exists(mock_uow, user_service):
    user_id = 1
    tag_data = UserTagCreate(user_id=user_id, name="hawktuah")
    mock_uow.user_tags.find_one.return_value = {"name": "hawktuah"}

    with pytest.raises(HTTPException) as exc_info:
        await user_service.create_user_tag(mock_uow, tag_data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Tag with this name already exists"


@pytest.mark.asyncio
async def test_update_user_tag(mock_uow, user_service):
    user_id = 1
    old_tag_name = "HawkTuah"
    new_tag_data = UserTagUpdate(name="fortnite battlepass")

    mock_uow.user_tags.find_one.side_effect = [
        {"name": "HawkTuah"},
        None
    ]

    mock_uow.user_tags.update.return_value = {"name": "fortnite battlepass"}

    updated_tag = await user_service.update_user_tag(mock_uow, new_tag_data, user_id, old_tag_name)

    assert updated_tag["name"] == "fortnite battlepass"
    mock_uow.user_tags.update.assert_called_once_with({"user_id": user_id, "name": old_tag_name},
                                                      new_tag_data.model_dump(exclude_none=True))


@pytest.mark.asyncio
async def test_delete_user_tag(mock_uow, user_service):
    user_id = 1
    tag_name = "HawkTuah"
    mock_uow.user_tags.find_one.return_value = {"name": "HawkTuah"}
    mock_uow.user_tags.delete.return_value = {"name": "HawkTuah"}

    deleted_tag = await user_service.delete_user_tag(mock_uow, user_id, tag_name)

    assert deleted_tag["name"] == "HawkTuah"
    mock_uow.user_tags.delete.assert_called_once_with({"user_id": user_id, "name": tag_name})
