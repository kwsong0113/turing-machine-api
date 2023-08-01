from .base import BaseCRUD, get_crud_function
from app.models.game import Game, GameCreate, GameUpdate


class GameCRUD(BaseCRUD[Game, GameCreate, GameUpdate]):
    pass


get_game_crud = get_crud_function(Game, GameCRUD)
