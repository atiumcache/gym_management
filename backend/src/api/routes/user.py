from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List, Optional

from src.database import get_db
from src.models.user import User
from src.schema.user import UserCreate, UserResponse, UserUpdate


def fetch_all_users(db: Session = Depends(get_db)) -> List[Optional[UserResponse]]:
    """Fetches all users.

    Args:
        db: The db session. Defaults to Depends(get_db).

    Returns:
        List of UserResponse models.
    """
