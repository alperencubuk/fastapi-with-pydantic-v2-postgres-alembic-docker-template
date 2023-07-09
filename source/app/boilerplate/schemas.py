from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from source.app.boilerplate.enums import Order, Sort
from source.core.schemas import PageSchema, ResponseSchema


class BoilerplateRequest(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class BoilerplateCreate(BoilerplateRequest):
    pass


class BoilerplateResponse(ResponseSchema):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    create_date: datetime
    update_date: datetime

    model_config = ConfigDict(from_attributes=True)


class BoilerplateUpdateRequest(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class BoilerplateUpdate(BoilerplateUpdateRequest):
    pass


class BoilerplatePage(PageSchema):
    boilerplate: list[BoilerplateResponse]


class BoilerplatePagination(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=0)
    sort: Sort = Sort.ID
    order: Order = Order.ASC


class BoilerplateId(BaseModel):
    boilerplate_id: int
