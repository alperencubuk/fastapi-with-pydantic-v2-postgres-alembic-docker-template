from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from source.core.database import database_health, get_db
from source.core.routers import api_router
from source.core.schemas import HealthSchema
from source.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title=settings.APP_TITLE, version=settings.VERSION, lifespan=lifespan)

app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthSchema, tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    return {"api": True, "database": await database_health(db=db)}
