from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.security import pwd_context

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

    def get_many(self, db: Session, *args, **kwargs) -> List[Optional[ORMModel]]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).all()

    def create(self, db: Session, obj_create: Type[BaseModel]) -> ORMModel:
        """Create a new record in the db.

        Args:
            db: The db session.
            data_obj: The data for creating the new record (Pydantic model).

        Returns:
            The newly created record.
        """
        obj_create_data = obj_create.model_dump(exclude_none=True, exclude_unset=True)
        if "password" in obj_create_data.keys():
            obj_create_data["hashed_password"] = pwd_context.hash(
                obj_create_data.pop("password")
            )
        db_obj = self._model(**obj_create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ORMModel,
        obj_update: Type[BaseModel],
    ) -> ORMModel:
        """
        Updates a record in the database.

        Parameters:
            db: The database session.
            db_obj: The database object to be updated.
            obj_update: The updated data for the object

        Returns:
            ORMModel: The updated database object.
        """
        # Convert model to dict
        obj_update_data = obj_update.model_dump()

        # Update all fields
        for field, value in obj_update_data.items():
            setattr(db_obj, field, value)

        # Add to session and commit
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Type[BaseModel]) -> ORMModel:
        """Delete record from db.

        Args:
            db: The db session
            db_obj: The object to be deleted

        Returns:
            The deleted object.
        """
        db.delete(db_obj)
        db.commit()
        return db_obj
