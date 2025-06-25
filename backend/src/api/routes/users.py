from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud.user import user_crud
from src.database import get_db
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.models.user import User
from src.api.dependencies import get_current_admin

router = APIRouter()


@router.get(
    "/all", response_model=List[Optional[UserResponse]], status_code=status.HTTP_200_OK
)
def fetch_all_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)
) -> List[Optional[UserResponse]]:
    """Fetches all users.

    Args:
        db: The db session. Defaults to Depends(get_db).

    Returns:
        List of UserResponse models.
    """
    users = user_crud.get_many(db)
    result = []
    for user in users:
        result.append(UserResponse.from_orm(user))
    return result
