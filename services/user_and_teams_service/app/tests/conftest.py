from contextlib import ExitStack

import pytest
import pytest_asyncio
from core.auth import get_current_user
from create_fastapi_app import init_app
from database.models.user import User
from database.session import get_db, sessionmanager
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from starlette.testclient import TestClient

test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=test_db.version,
        password=pg_password,
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def db_override_factory():
        async def get_db_override():
            async with sessionmanager.session() as session:
                yield session

        return get_db_override

    def override_get_current_superadmin():
        user = User(
            id=1,
            email="test@gmail.com",
            first_name="Maxim",
            second_name="Huy",
            hashed_password="1234576",
            role="user",
        )

        return user

    app.dependency_overrides[get_db] = db_override_factory
    app.dependency_overrides[get_current_user] = override_get_current_superadmin
