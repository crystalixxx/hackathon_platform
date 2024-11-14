import uuid
from datetime import datetime
from ..database.schemas.user import TUserCreate


def test_user_create():
    """Проверяет, что можно создать пользователя и что все поля заполнены корректно"""

    user_data = {
        "id": uuid.uuid4(),
        "email": "test@example.com",
        "first_name": "John",
        "second_name": "Doe",
        "hashed_password": "hashedpassword123",
        "role": "admin",
        "link_cv": "https://example.com/cv",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        # datetime.datetime.utcnow() is deprecated and scheduled for removal in a
        # future version. Use timezone-aware objects to represent datetime in UTC: datetime.datetime.now(datetime.UTC).
    }

    user = TUserCreate(**user_data)

    assert user.id == user_data["id"]
    assert user.email == user_data["email"]
    assert user.first_name == user_data["first_name"]
    assert user.second_name == user_data["second_name"]
    assert user.hashed_password == user_data["hashed_password"]
    assert user.role == user_data["role"]
    assert user.link_cv == user_data["link_cv"]
    assert user.created_at == user_data["created_at"]
    assert user.updated_at == user_data["updated_at"]
