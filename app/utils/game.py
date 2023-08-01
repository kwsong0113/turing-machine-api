from app.crud import GameCRUD
from app.models import GameStatus


async def isolate_game(game_id: int, game_crud: GameCRUD) -> None:
    await game_crud.update(game_id, {"status": GameStatus.PLAYING})
