from app.crud.user import UserCRUD


async def leave_game(user_id: int, user_crud: UserCRUD) -> None:
    await user_crud.update(user_id, {"game_id": None})
