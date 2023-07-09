from fastapi import APIRouter, Depends

from source.app.boilerplate.views import boilerplate_router
from source.core.auth import api_key_auth

api_router = APIRouter()

api_router.include_router(boilerplate_router, dependencies=[Depends(api_key_auth)])
