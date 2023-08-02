from enum import StrEnum

from app.crud import GameCRUD, ProblemCRUD
from app.models import GameStatus, Problem
import aiohttp
import asyncio

from app.models import ProblemCreate


async def isolate_game(game_id: int, game_crud: GameCRUD) -> None:
    await game_crud.update(game_id, {"status": GameStatus.PLAYING})


async def make_request(url: str, params: dict[str, any]):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            json = await response.json()
            return json


async def generate_problem(difficulty: int, num_verifiers: int) -> ProblemCreate:
    result = await make_request(
        "https://turingmachine.info/api/api.php",
        {"m": 0, "d": difficulty, "n": num_verifiers},
    )
    return ProblemCreate(
        id=result["hash"],
        verifiers=result["ind"],
        laws=result["law"],
        code=result["code"],
    )


class GuessResultType(StrEnum):
    BOTH_WRONG = "BOTH_WRONG"
    BOTH_CORRECT = "BOTH_CORRECT"
    WINNER = "WINNER"
    NO_THUMB = "NO_THUMB"


class GuessResult:
    def __init__(self, result_type: GuessResultType, winner_id: int | None = None):
        self.result_type = result_type
        self.winner_id = winner_id


async def get_guess_result(
    problem_id: str, guesses: dict[int, int], problem_crud: ProblemCRUD
) -> GuessResult:
    problem = await problem_crud.get(problem_id)
    thumb_up_guesses = {id: num for id, num in guesses.items() if num != 0}
    thumb_down_guesses = {id: num for id, num in guesses.items() if num == 0}
    correct_guesses = {
        id: num for id, num in thumb_up_guesses.items() if num == problem.code
    }
    match len(correct_guesses):
        case 0:
            if len(thumb_up_guesses) == 0:
                return GuessResult(GuessResultType.NO_THUMB)
            elif len(thumb_up_guesses) == 1:
                return GuessResult(
                    GuessResultType.WINNER, list(thumb_down_guesses.keys())[0]
                )
            else:
                return GuessResult(GuessResultType.BOTH_WRONG)

        case 1:
            return GuessResult(GuessResultType.WINNER, list(correct_guesses.keys())[0])
        case 2:
            return GuessResult(GuessResultType.BOTH_CORRECT)
