from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class GameBase(SQLModel):
    pass


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(back_populates="game")


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass
