from fastapi import FastAPI

from app.core.config import settings
from app.api.router import api_router

app = FastAPI(
    title=f"Turing Machine API - {'Development' if settings.DEV else 'Production'}",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
