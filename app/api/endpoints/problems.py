from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from starlette import status

from app.api.response import DetailResponse
from app.crud.problem import ProblemCRUD, get_problem_crud

from app.models import Problem

router = APIRouter()


@router.get(
    "/{problem_id}",
    response_model=Problem,
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def get_problem(
    problem_id: int, problem_crud: ProblemCRUD = Depends(get_problem_crud)
):
    problem = await problem_crud.get(problem_id)
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return problem


@router.get("/", response_model=list[Problem])
async def get_problems(problem_crud: ProblemCRUD = Depends(get_problem_crud)):
    return await problem_crud.get_multi()
