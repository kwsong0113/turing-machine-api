from enum import StrEnum
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class GameStatus(StrEnum):
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    ENDED = "ENDED"


class GameBase(SQLModel):
    status: GameStatus = Field(default="WAITING")
    problem_id: Optional[str] = Field(default=None)


class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(
        back_populates="game", sa_relationship_kwargs={"lazy": "selectin"}
    )


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass
