from fastapi import WebSocket

from app.crud import ProblemCRUD, GameCRUD, UserCRUD
from app.utils.game import isolate_game, assign_problem, end_game
from app.utils.problem import generate_problem, get_guess_result, GuessResultType
from app.utils.user import leave_game


class GameManager:
    def __init__(self, game_id: int):
        self.game_id = game_id
        self.active_user_connections: dict[int, WebSocket] = {}
        self.stage = -1
        self.active_user_guesses: dict[int, int] = {}
        self.problem_id: str | None = None
        self.game_crud: GameCRUD | None = None
        self.problem_crud: ProblemCRUD | None = None
        self.user_crud: UserCRUD | None = None
        self.cleaning: bool = False

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_user_connections[user_id] = websocket
        if len(self.active_user_connections) == 2:
            await isolate_game(self.game_id, self.game_crud)
            await self.promote_stage()
            await self.send_personal_message(user_id, {"type": "PROBLEM"})

    def set_cruds(
        self, game_crud: GameCRUD, problem_crud: ProblemCRUD, user_crud: UserCRUD
    ):
        if self.game_crud is None:
            self.game_crud = game_crud
        if self.problem_crud is None:
            self.problem_crud = problem_crud
        if self.user_crud is None:
            self.user_crud = user_crud

    async def disconnect(self, user_id: int):
        del self.active_user_connections[user_id]
        self.active_user_guesses.pop(user_id)

    async def cleanup(self, disconnected_user_id: int | None = None):
        if self.cleaning:
            return
        self.cleaning = True
        for user_id, websocket in self.active_user_connections.items():
            if user_id != disconnected_user_id:
                await websocket.close()
        for user_id in self.active_user_connections:
            await leave_game(user_id, self.user_crud)
        await end_game(self.game_id, self.game_crud)
        connection_manager.disconnect(self.game_id)

    async def broadcast(self, json: dict[str, any]):
        for websocket in self.active_user_connections.values():
            await websocket.send_json(json)

    async def send_personal_message(self, user_id: int, json: dict[str, any]):
        await self.active_user_connections[user_id].send_json(json)

    async def on_receive(self, data: dict[str, any], user_id: int):
        match data["type"]:
            case "PROBLEM":
                problem = await generate_problem(
                    data["difficulty"], data["num_verifiers"]
                )
                await assign_problem(
                    self.game_id, problem, self.game_crud, self.problem_crud
                )
                self.problem_id = problem.id
                await self.broadcast({"type": "PROBLEM_ID", "id": self.problem_id})
                await self.promote_stage()
            case "THUMB":
                self.active_user_guesses[user_id] = (
                    data["num"] if data["thumb"] == "UP" else 0
                )
                if len(self.active_user_guesses) == 2:
                    result = await get_guess_result(
                        self.problem_id, self.active_user_guesses, self.problem_crud
                    )

                    if result.result_type == GuessResultType.NO_THUMB:
                        await self.promote_stage()
                    else:
                        await self.broadcast({"type": "RESULT", **result.__dict__})
                        await self.cleanup()

    async def promote_stage(self):
        self.stage += 1
        self.active_user_guesses = {}
        await self.broadcast({"type": "STAGE", "stage": self.stage})


class ConnectionMananger:
    def __init__(self):
        self.game_mananagers: dict[int, GameManager] = {}

    def get_game_mananger(self, game_id: int) -> GameManager:
        if game_id not in self.game_mananagers:
            self.game_mananagers[game_id] = GameManager(game_id)
        return self.game_mananagers[game_id]

    async def connect(
        self,
        websocket: WebSocket,
        game_id: int,
        user_id: int,
        game_crud: GameCRUD,
        problem_crud: ProblemCRUD,
        user_crud: UserCRUD,
    ) -> GameManager:
        game_manager = self.get_game_mananger(game_id)
        game_manager.set_cruds(game_crud, problem_crud, user_crud)
        await game_manager.connect(websocket, user_id)
        return game_manager

    def disconnect(self, game_id: int):
        del self.game_mananagers[game_id]


connection_manager = ConnectionMananger()
