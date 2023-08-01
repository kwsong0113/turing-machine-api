from fastapi import Depends

from app.crud import GameCRUD, get_game_crud
from app.models import GameStatus


async def isolate_game(game_id: int, game_crud) -> None:
    await game_crud.update(game_id, {"status": GameStatus.PLAYING})
