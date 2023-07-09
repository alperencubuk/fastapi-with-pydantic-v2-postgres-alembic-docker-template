from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: int


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
