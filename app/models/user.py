from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .game import Game


class UserBase(SQLModel):
    username: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: Optional[int] = Field(default=None, foreign_key="game.id")

    game: Optional["Game"] = Relationship(back_populates="users")


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
