import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, drop_database

from source.core.database import Base, get_db
from source.core.settings import settings
from source.main import app

test_db_uri = f"{settings.POSTGRES_URI}_test"
engine = create_engine(test_db_uri)
SessionLocal = sessionmaker(bind=engine)


def get_test_db() -> Session:
    test_db = SessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db():
    create_database(test_db_uri)
    Base.metadata.create_all(bind=engine)
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
    test_db = SessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()
