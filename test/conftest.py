import asyncio
from typing import Any, AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, drop_database

from source.core.database import Base, get_db
from source.core.settings import settings
from source.main import app

engine = create_async_engine(f"postgresql+asyncpg://{settings.POSTGRES_URI}_test")
SessionLocal = async_sessionmaker(bind=engine)


async def get_test_db() -> AsyncGenerator[AsyncSession, Any]:
    test_db = SessionLocal()
    try:
        yield test_db
    finally:
        await test_db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db():
    test_db_uri = f"postgresql://{settings.POSTGRES_URI}_test"
    create_database(test_db_uri)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    drop_database(test_db_uri)


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={settings.API_KEY_HEADER: settings.API_KEY},
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db():
    async for db in get_test_db():
        yield db
