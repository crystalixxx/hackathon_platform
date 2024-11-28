import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database.models.base import Base
from app.database.session import get_db
from app.main import app

DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncTestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def db_session(prepare_database):
    async with AsyncTestingSessionLocal() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture(scope="session")
async def client(db_session) -> AsyncClient:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        base_url="http://0.0.0.0:8000", transport=ASGITransport(app=app)
    ) as c:
        yield c
    app.dependency_overrides.clear()
