from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.api.response import DetailResponse
from app.crud.user import UserCRUD, get_user_crud
from app.models.user import User, UserCreate

router = APIRouter()


@router.get(
    "/{id}",
    response_model=User,
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def get_user(user_id: int, user_crud: UserCRUD = Depends(get_user_crud)):
    user = await user_crud.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.get("/", response_model=list[User])
async def get_users(user_crud: UserCRUD = Depends(get_user_crud)):
    return await user_crud.get_multi()


@router.post("/", response_model=User)
async def create_user(
    user_in: UserCreate, user_crud: UserCRUD = Depends(get_user_crud)
):
    return await user_crud.create(user_in)


@router.delete(
    "/{user_id}",
    response_model=User,
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def delete_user(user_id: int, user_crud: UserCRUD = Depends(get_user_crud)):
    user = await user_crud.remove(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
