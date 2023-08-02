from .base import BaseCRUD, get_crud_function
from app.models.problem import Problem, ProblemCreate, ProblemUpdate


class ProblemCRUD(BaseCRUD[Problem, ProblemCreate, ProblemUpdate]):
    pass


get_problem_crud = get_crud_function(Problem, ProblemCRUD)
