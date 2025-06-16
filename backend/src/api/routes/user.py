from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List, Optional

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse, UserUpdate

from src.crud.user import user_crud

router = APIRouter()


@router.get(
    "/all", response_model=List[Optional[UserResponse]], status_code=status.HTTP_200_OK
)
def fetch_all_users(db: Session = Depends(get_db)) -> List[Optional[UserResponse]]:
    """Fetches all users.

    Args:
        db: The db session. Defaults to Depends(get_db).

    Returns:
        List of UserResponse models.
    """
    return user_crud.get_many(db)
