from src.crud.base import CRUDRepository
from src.models.user import User, Role, UserRole

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import Optional, List, Union


class UserCRUDRepository(CRUDRepository):
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            db: The db session
            email: The email of the user

        Returns:
            The user found by email, or None if not found.
        """
        return self.get_one(db, self._model.email == email)

    def add_role(self, db: Session, user_id: int, role_name: str) -> bool:
        """Add a role to a user.

        Args:
            db: The db session
            user_id: The user.id primary key
            role_name: Name of role to add
                ('client', 'admin', 'coach')

        Returns:
            True if role added successfully, False otherwise.
        """
        try:
            # Get role by name
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                return False

            existing = (
                db.query(UserRole)
                .filter(UserRole.role_id == role.id, UserRole.user_id == user_id)
                .first()
            )

            if existing:
                return False  # Role already assigned

            user_role = UserRole(user_id=user_id, role_id=role.id)
            db.add(user_role)
            db.commit()
            return True

        except IntegrityError:
            db.rollback()
            return False

    def remove_role(self, db: Session, user_id: int, role_name: str) -> bool:
        """Remove a role from a user.

        Args:
            db: The database session
            user_id: ID of the user
            role_name: Name of the role to remove

        Returns:
            True if role was removed successfully, False otherwise
        """
        try:
            # Get the role by name
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                return False

            # Find and delete the user-role relationship
            user_role = (
                db.query(UserRole)
                .filter(UserRole.user_id == user_id, UserRole.role_id == role.id)
                .first()
            )

            if not user_role:
                return False  # Role not assigned to user

            db.delete(user_role)
            db.commit()
            return True

        except Exception:
            db.rollback()
            return False
