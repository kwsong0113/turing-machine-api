from app.crud import GameCRUD, ProblemCRUD
from app.models import GameStatus, Problem, ProblemCreate


async def isolate_game(game_id: int, game_crud: GameCRUD) -> None:
    await game_crud.update(game_id, {"status": GameStatus.PLAYING})


async def assign_problem(
    game_id: int, problem: ProblemCreate, game_crud: GameCRUD, problem_crud: ProblemCRUD
) -> None:
    problem_in_db = await problem_crud.get(problem.id)
    if problem_in_db is None:
        await problem_crud.create(problem)
    await game_crud.update(game_id, {"problem_id": problem.id})
