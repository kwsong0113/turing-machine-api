from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Body,
)
from starlette import status

from app.api.response import DetailResponse
from app.crud.problem import ProblemCRUD, get_problem_crud

from app.models import Problem
from app.utils.law import verify

router = APIRouter()


@router.get(
    "/{problem_id}",
    response_model=Problem,
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def get_problem(
    problem_id: str, problem_crud: ProblemCRUD = Depends(get_problem_crud)
):
    problem = await problem_crud.get(problem_id)
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return problem


@router.get("/", response_model=list[Problem])
async def get_problems(problem_crud: ProblemCRUD = Depends(get_problem_crud)):
    return await problem_crud.get_multi()


@router.post(
    "/question/{problem_id}",
    response_model=list[bool],
    responses={status.HTTP_404_NOT_FOUND: {"model": DetailResponse}},
)
async def question(
    problem_id: str,
    proposal: Annotated[int, Body()],
    verifier_indices: list[int],
    problem_crud: ProblemCRUD = Depends(get_problem_crud),
):
    problem = await problem_crud.get(problem_id)
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return [verify(problem.laws[index], proposal) for index in verifier_indices]
