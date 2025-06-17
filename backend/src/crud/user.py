from typing import List, Optional, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.base import CRUDRepository
from src.models.user import Role, User, UserRole


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

    def get_user_roles(self, db: Session, user_id: int) -> List[str]:
        """Get all roles for a user.

        Args:
            db: The database session
            user_id: ID of the user

        Returns:
            List of role names
        """
        roles = (
            db.query(Role.name).join(UserRole).filter(UserRole.user_id == user_id).all()
        )
        return [role.name for role in roles]

    def has_role(self, db: Session, user_id: int, role_name: str) -> bool:
        """Check if a user has a specific role.

        Args:
            db: The database session
            user_id: ID of the user
            role_name: Name of the role to check

        Returns:
            True if user has the role, False otherwise
        """
        count = (
            db.query(UserRole)
            .join(Role)
            .filter(UserRole.user_id == user_id, Role.name == role_name)
            .count()
        )
        return count > 0

    def set_roles(self, db: Session, user_id: int, role_names: List[str]) -> bool:
        """Set user's roles (replaces all existing roles).

        Args:
            db: The database session
            user_id: ID of the user
            role_names: List of role names to assign

        Returns:
            True if roles were set successfully, False otherwise
        """
        try:
            # Remove all existing roles
            db.query(UserRole).filter(UserRole.user_id == user_id).delete()

            # Add new roles
            for role_name in role_names:
                role = db.query(Role).filter(Role.name == role_name).first()
                if role:
                    user_role = UserRole(user_id=user_id, role_id=role.id)
                    db.add(user_role)

            db.commit()
            return True

        except Exception:
            db.rollback()
            return False


user_crud = UserCRUDRepository(User)
