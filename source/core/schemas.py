from pydantic import BaseModel
from pydantic.config import ConfigDict


class ResponseSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PageSchema(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class ExceptionSchema(BaseModel):
    detail: str


class HealthSchema(BaseModel):
    api: bool
    database: bool
