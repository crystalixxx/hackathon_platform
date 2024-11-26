from app.core.config import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(config.database_connection_url)

session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    yield session_local()
