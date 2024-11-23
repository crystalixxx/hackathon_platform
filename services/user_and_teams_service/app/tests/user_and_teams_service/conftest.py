import jwt
import pytest
from app.core.auth import get_current_user
from app.core.config import config
from app.database.models.base import Base
from app.database.models.user import User
from app.database.session import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session


def create_test_jwt_token(user_id: int):
    token_data = {"sub": str(user_id), "exp": config.ACCESS_TOKEN_EXPIRE_MINUTES}
    token = jwt.encode(token_data, config.SECURITY_KEY, algorithm=config.ALGORITHM)
    return token


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture()
def client(session: Session):
    def get_session_override():
        return session

    def override_get_current_superadmin():
        db = get_session_override()

        user = User(
            id=1,
            username="test@gmail.com",
            hashed_password="1234576",
            is_superadmin=True,
            is_blocked=False,
        )

        return user

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_current_user] = override_get_current_superadmin

    client = TestClient(app)
    token = create_test_jwt_token(1)
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client

    app.dependency_overrides.clear()
