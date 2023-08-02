from typing import List

from sqlalchemy import Column
from sqlmodel import SQLModel, Field, ARRAY, Integer


class ProblemBase(SQLModel):
    id: str = Field(primary_key=True)
    verifiers: List[int] = Field(sa_column=Column(ARRAY(Integer())))
    laws: List[int] = Field(sa_column=Column(ARRAY(Integer())))
    code: int


class Problem(ProblemBase, table=True):
    pass


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    pass
