from fastapi import APIRouter, Depends

from app.crud import (
    UserCRUD,
    GameCRUD,
    get_user_crud,
    get_game_crud,
    ProblemCRUD,
    get_problem_crud,
)

router = APIRouter()


@router.get(
    "/",
    response_model=bool,
)
async def health_check(
    user_crud: UserCRUD = Depends(get_user_crud),
    game_crud: GameCRUD = Depends(get_game_crud),
    problem_crud: ProblemCRUD = Depends(get_problem_crud),
):
    users = await user_crud.get_multi()
    games = await game_crud.get_multi()
    problems = await problem_crud.get_multi()

    return (
        isinstance(users, list)
        and isinstance(games, list)
        and isinstance(problems, list)
    )
