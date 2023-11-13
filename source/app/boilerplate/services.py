from math import ceil

from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
    boilerplate_id: int, db: AsyncSession
) -> BoilerplateResponse | None:
    if boilerplate := await db.get(BoilerplateModel, boilerplate_id):
        return BoilerplateResponse.model_validate(boilerplate)
    return None


async def list_boilerplate(
    page: int, size: int, sort: Sort, order: Order, db: AsyncSession
) -> BoilerplatePage:
    order = asc(sort) if order == Order.ASC.value else desc(sort)
    boilerplates = await db.scalars(
        select(BoilerplateModel).order_by(order).offset((page - 1) * size).limit(size)
    )
    total = await db.scalar(select(func.count(BoilerplateModel.id)))

    boilerplate_list = [
        BoilerplateResponse.model_validate(boilerplate)
        for boilerplate in boilerplates.all()
    ]
    return BoilerplatePage(
        boilerplate=boilerplate_list,
        page=page,
        size=size,
        total=total,
        pages=(ceil(total / size) if size else 1),
    )


async def create_boilerplate(
    boilerplate: BoilerplateRequest, db: AsyncSession
) -> BoilerplateResponse | None:
    try:
        boilerplate = BoilerplateModel(
            **BoilerplateCreate(**boilerplate.model_dump()).model_dump()
        )
        db.add(boilerplate)
        await db.commit()
        await db.refresh(boilerplate)
        return BoilerplateResponse.model_validate(boilerplate)
    except IntegrityError:
        return None


async def update_boilerplate(
    boilerplate: BoilerplateModel,
    boilerplate_update: BoilerplateUpdateRequest,
    db: AsyncSession,
) -> BoilerplateResponse | None:
    try:
        fields_to_update = (
            BoilerplateUpdate(**boilerplate_update.model_dump()).model_dump().items()
        )
        for key, value in fields_to_update:
            if value is not None:
                setattr(boilerplate, key, value)
        await db.commit()
        await db.refresh(boilerplate)
        return BoilerplateResponse.model_validate(boilerplate)
    except IntegrityError:
        return None


async def delete_boilerplate(boilerplate_id: int, db: AsyncSession) -> bool:
    if boilerplate := await db.get(BoilerplateModel, boilerplate_id):
        await db.delete(boilerplate)
        await db.commit()
        return True
    return False


async def get_db_boilerplate(
    boilerplate_id: int, db: AsyncSession
) -> BoilerplateModel | None:
    return await db.get(BoilerplateModel, boilerplate_id)
