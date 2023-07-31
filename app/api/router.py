from fastapi import APIRouter
from .endpoints import teams, heroes

api_router = APIRouter()

routers = [
    (teams.router, "teams", "teams"),
    (heroes.router, "heroes", "heroes"),
]

for router, prefix, tag in routers:
    api_router.include_router(router, prefix=f"/{prefix}", tags=[tag] if tag else None)
