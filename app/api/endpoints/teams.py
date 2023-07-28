from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.team import Team

router = APIRouter()


@router.get("/", response_model=list[Team])
async def get_teams(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Team))
    teams = result.scalars().all()
    return teams
