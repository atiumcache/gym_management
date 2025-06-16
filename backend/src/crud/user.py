from src.crud.base import CRUDRepository
from src.models.user import User

from sqlalchemy.orm import Session

from typing import Optional

class UserCRUDRepository(CRUDRepository):
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            db: The db session. 
            email: The email of the user.

        Returns:
            The user found by email, or None if not found.
        """
        return self.get_one(db, self._model.email == email)
