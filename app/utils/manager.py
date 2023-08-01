from fastapi import WebSocket

from app.crud.game import GameCRUD
from app.utils.game import isolate_game


class GameManager:
    def __init__(self, game_id: int):
        self.game_id = game_id
        self.active_user_connections: dict[int, WebSocket] = {}
        self.stage = -1
        self.active_user_guesses: dict[int, int] = {}
        self.problem_id: int | None = None
        self.game_crud: GameCRUD | None = None

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_user_connections[user_id] = websocket
        if len(self.active_user_connections) == 2:
            # TODO: call isolate_game util
            await isolate_game(self.game_id, self.game_crud)
            await self.promote_stage()
            await self.send_personal_message(user_id, {"type": "PROBLEM"})

    def set_game_crud(self, game_crud: GameCRUD):
        if self.game_crud is None:
            self.game_crud = game_crud

    async def disconnect(self, user_id: int):
        del self.active_user_connections[user_id]
        self.active_user_guesses.pop(user_id)

    async def broadcast(self, json: dict[str, any]):
        for websocket in self.active_user_connections.values():
            await websocket.send_json(json)

    async def send_personal_message(self, user_id: int, json: dict[str, any]):
        await self.active_user_connections[user_id].send_json(json)

    async def on_receive(self, data: dict[str, any], user_id: int):
        match data["type"]:
            case "PROBLEM":
                # TODO: set problem_id
                # TODO: call generate_and_assign_problem util
                await self.broadcast({"type": "PROBLEM_ID", "id": self.problem_id})
                await self.promote_stage()
            case "THUMB":
                self.active_user_guesses[user_id] = (
                    data["num"] if data["thumb"] == "UP" else 0
                )
                if len(self.active_user_guesses) == 2:
                    pass
                    # TODO: call get_results util
                    # Results can be promote, no winner, winner
                    # TODO: promote stage or broadcast result
                    await connection_manager.disconnect(self.game_id)

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
        self, websocket: WebSocket, game_id: int, user_id: int, game_crud: GameCRUD
    ) -> GameManager:
        game_manager = self.get_game_mananger(game_id)
        game_manager.set_game_crud(game_crud)
        await game_manager.connect(websocket, user_id)
        return game_manager

    async def disconnect(self, game_id: int):
        del self.game_mananagers[game_id]


connection_manager = ConnectionMananger()
