from typing import List
from sqlmodel import SQLModel, Field


class ProblemBase(SQLModel):
    id: str = Field(primary_key=True)
    verifiers: List[int]
    laws: List[int]


class Problem(ProblemBase, table=True):
    pass


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    pass
