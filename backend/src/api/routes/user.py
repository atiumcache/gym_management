from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.user import user_crud
from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The created user"
)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a new user.

    Args:
        user: The user data to create
        db: The database session. Defaults to Depends(get_db).


    Returns:
        The created user

    Raises:
        HTTPException: If a user with the email already exists
    """
    try:
        # Check if user with email already exists
        if user_crud.get_user_by_email(db, email=user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        # Create the user
        db_user = user_crud.create(db, user)
        return db_user
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        ) from e


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
