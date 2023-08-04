from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    Body,
)
from starlette import status

from app.api.response import DetailResponse
from app.crud import (
    UserCRUD,
    GameCRUD,
    get_user_crud,
    get_game_crud,
    ProblemCRUD,
    get_problem_crud,
)
from app.models.game import Game, GameCreate, GameStatus
from app.utils.manager import connection_manager

router = APIRouter()


@router.get(
    "/{game_id}",
    response_model=Game,
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def get_game(game_id: int, game_crud: GameCRUD = Depends(get_game_crud)):
    game = await game_crud.get(game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return game


@router.get("/", response_model=list[Game])
async def get_games(game_crud: GameCRUD = Depends(get_game_crud)):
    return await game_crud.get_multi()


@router.post("/", response_model=Game)
async def create_game(
    game_in: GameCreate, game_crud: GameCRUD = Depends(get_game_crud)
):
    return await game_crud.create(game_in)


@router.post(
    "/start",
    response_model=Game,
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def start_game(
    user_id: Annotated[int, Body(embed=True)],
    game_crud: GameCRUD = Depends(get_game_crud),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    user = await user_crud.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user.game_id:
        await user_crud.update(user_id, {"game_id": None})

    all_games = await game_crud.get_multi()
    first_open_game = next(
        (
            game
            for game in all_games
            if len(game.users) < 2 and game.status == GameStatus.WAITING
        ),
        None,
    )
    if first_open_game is None:
        first_open_game = await game_crud.create(GameCreate())

    await user_crud.update(user_id, {"game": first_open_game})
    return first_open_game


@router.websocket("/ws/{game_id}/{user_id}")
async def game_websocket(
    websocket: WebSocket,
    game_id: int,
    user_id: int,
    game_crud: GameCRUD = Depends(get_game_crud),
    problem_crud: ProblemCRUD = Depends(get_problem_crud),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    game_manager = await connection_manager.connect(
        websocket, game_id, user_id, game_crud, problem_crud, user_crud
    )

    while True:
        try:
            data = await websocket.receive_json()
            await game_manager.on_receive(data, user_id)

        except WebSocketDisconnect:
            await game_manager.cleanup(user_id)
            break
