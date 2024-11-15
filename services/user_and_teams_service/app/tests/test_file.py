from ..database.schemas.user import UserBase


def test_user():
    """Проверяет, что все поля заполнены корректно"""

    user_data = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "admin",
        "link_cv": "https://example.com/cv",
    }

    user = UserBase(**user_data)

    assert user.email == user_data["email"]
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.role == user_data["role"]
    assert user.link_cv == user_data["link_cv"]
