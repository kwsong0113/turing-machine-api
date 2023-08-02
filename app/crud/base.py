from typing import (
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    Callable,
    Awaitable,
)
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int | str) -> Optional[ModelType]:
        obj = await self.session.get(self.model, id)
        return obj

    async def get_multi(
        self, skip: int = 0, limit: int | None = None
    ) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        results = await self.session.execute(statement)
        return results.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
        self, id: int | str, obj_in: Union[UpdateSchemaType, Dict[str, any]]
    ) -> Optional[ModelType]:
        db_obj = await self.get(id)
        if db_obj is None:
            return None
        update_data = (
            obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def remove(self, id: int | str) -> Optional[ModelType]:
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()

        return obj


CRUDType = TypeVar("CRUDType", bound=BaseCRUD)


def get_crud_function(
    model: Type[ModelType], crud: Type[CRUDType]
) -> Callable[[AsyncSession], Awaitable[CRUDType]]:
    async def get_crud(session: AsyncSession = Depends(get_session)):
        return crud(model, session)

    return get_crud
