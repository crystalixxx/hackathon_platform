import asyncio
from contextlib import ExitStack

import pytest
from httpx import AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app import init_app
from app.database.session import get_db, sessionmanager


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
async def client(app):
    async with AsyncClient(
        app=app, base_url="http://user_and_teams_service.localhost"
    ) as c:
        yield c


postgresql_in_docker = factories.postgresql_noproc()


@pytest.fixture(scope="session")
def test_db(postgresql_in_docker):
    dbname = "test_db"
    version = postgresql_in_docker.version
    user = postgresql_in_docker.user
    host = postgresql_in_docker.host
    port = postgresql_in_docker.port
    password = postgresql_in_docker.password

    janitor = DatabaseJanitor(user, host, port, dbname, version, password)
    janitor.init()

    try:
        yield postgresql_in_docker
    finally:
        janitor.drop()


@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+asyncpg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override
