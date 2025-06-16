from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

ORMModel = TypeVar("ORMModel")


class CRUDRepository:
    """Base interface for CRUD operations."""

    def __init__(self, model: Type[ORMModel]) -> None:
        """Initialize the CRUD repository.

        Args:
            model: The ORM model to use for CRUD ops.
            See src.models.
        """
        self._model = model
        self._name = model.__name__

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ORMModel]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).first()

    def create(self, db: Session, obj_create: Type[BaseModel]) -> ORMModel:
        """Create a new record in the db.

        Args:
            db: The db session.
            data_obj: The data for creating the new record (Pydantic model).

        Returns:
            The newly created record.
        """
        obj_create_data = obj_create.model_dump(exclude_none=True, exclude_unset=True)
        db_obj = self._model(**obj_create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
