from math import ceil

from sqlalchemy import asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from source.app.boilerplate.enums import Order, Sort
from source.app.boilerplate.models import BoilerplateModel
from source.app.boilerplate.schemas import (
    BoilerplateCreate,
    BoilerplatePage,
    BoilerplateRequest,
    BoilerplateResponse,
    BoilerplateUpdate,
    BoilerplateUpdateRequest,
)


async def get_boilerplate(
    boilerplate_id: int, db: Session
) -> BoilerplateResponse | None:
    if boilerplate := db.get(BoilerplateModel, boilerplate_id):
        return BoilerplateResponse.model_validate(boilerplate)
    return None


async def list_boilerplate(
    page: int, size: int, sort: Sort, order: Order, db: Session
) -> BoilerplatePage:
    order = asc(sort) if order == Order.ASC.value else desc(sort)
    boilerplate_list = (
        db.query(BoilerplateModel).order_by(order).offset((page - 1) * size).limit(size)
    )
    total = boilerplate_list.count()
    boilerplate_list = [
        BoilerplateResponse.model_validate(boilerplate)
        for boilerplate in boilerplate_list.all()
    ]
    return BoilerplatePage(
        boilerplate=boilerplate_list,
        page=page,
        size=size,
        total=total,
        pages=(ceil(total / size) if size else 1),
    )


async def create_boilerplate(
    boilerplate: BoilerplateRequest, db: Session
) -> BoilerplateResponse | None:
    try:
        boilerplate = BoilerplateModel(
            **BoilerplateCreate(**boilerplate.model_dump()).model_dump()
        )
        db.add(boilerplate)
        db.commit()
        db.refresh(boilerplate)
        return BoilerplateResponse.model_validate(boilerplate)
    except IntegrityError:
        return None


async def update_boilerplate(
    boilerplate_id: int,
    boilerplate: BoilerplateUpdateRequest,
    db: Session,
) -> BoilerplateResponse | None:
    try:
        fields_to_update = (
            BoilerplateUpdate(**boilerplate.model_dump()).model_dump().items()
        )
        if boilerplate := db.get(BoilerplateModel, boilerplate_id):
            for key, value in fields_to_update:
                if value is not None:
                    setattr(boilerplate, key, value)
            db.commit()
            db.refresh(boilerplate)
            return BoilerplateResponse.model_validate(boilerplate)
        return None
    except IntegrityError:
        return None


async def delete_boilerplate(boilerplate_id: int, db: Session) -> bool:
    if boilerplate := db.get(BoilerplateModel, boilerplate_id):
        db.delete(boilerplate)
        db.commit()
        return True
    return False
