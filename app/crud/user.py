from .base import BaseCRUD, get_crud_function
from app.models.user import User, UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    pass


get_user_crud = get_crud_function(User, UserCRUD)
