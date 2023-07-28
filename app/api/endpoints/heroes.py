from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.hero import Hero

router = APIRouter()


@router.get("/", response_model=list[Hero])
async def get_heroes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Hero))
    heroes = result.scalars().all()
    return heroes
