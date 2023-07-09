from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from source import BoilerplateModel


@pytest.mark.asyncio
async def test_create_boilerplate(client: AsyncClient):
    payload = {
        "email": "test_create@boilerplate.com",
        "first_name": "boiler",
        "last_name": "plate",
    }
    response = await client.post("/boilerplate/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_get_boilerplate(client: AsyncClient, db: Session):
    date = datetime.utcnow()
    payload = {
        "email": "test_get@boilerplate.com",
        "first_name": "boiler",
        "last_name": "plate",
        "create_date": date,
        "update_date": date,
    }
    boilerplate = BoilerplateModel(**payload)
    db.add(boilerplate)
    db.commit()
    db.refresh(boilerplate)
    response = await client.get(f"/boilerplate/{boilerplate.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
