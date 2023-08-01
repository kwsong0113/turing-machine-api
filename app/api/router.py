from fastapi import APIRouter
from .endpoints import users, games

api_router = APIRouter()

routers = [(users.router, "users", "users"), (games.router, "games", "games")]

for router, prefix, tag in routers:
    api_router.include_router(router, prefix=f"/{prefix}", tags=[tag] if tag else None)
