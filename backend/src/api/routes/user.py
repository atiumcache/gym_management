from typing import List, Optional, Sequence

from src.api.dependencies import get_current_active_user, get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.user import UserCRUDRepository, user_crud
from src.database import get_db
from src.models.user import User, RoleName
from src.schemas.user import UserCreate, UserResponse, UserUpdate, UserBase

router = APIRouter()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
    summary="Get all users",
    response_description="List of all users",
)
def get_all_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    try:
        users = user_crud.get_many(db=db)
        return [UserResponse.from_orm(user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Retrieve the current user",
    response_description="The current user",
)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> UserResponse:
    """Get Current user's information.

    This endpoint requires authentication.

    Args:
        current_user: The current user. Defaults to Depends(get_current_active_user).
        db: The db session. Defaults to Depends(get_db).

    Returns:
        The currently logged-in user based on their JWT token.
    """
    return current_user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The created user",
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
                detail="Email already registered",
            )

        # Create the user
        db_user = user_crud.create(db, user)
        return db_user

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create user"
        ) from e


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def fetch_one_user(
    user_id: int, db: Session = Depends(get_db)
) -> Optional[UserResponse]:
    """Fetch one user.

    Args:
        db: The db session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        UserResponse model.
    """
    db_user = user_crud.get_one(db=db, id=int(user_id))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a user (full update)",
    response_description="The updated user",
)
def update_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
) -> UserResponse:
    db_user = user_crud.get_one(db=db, id=int(user_id))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    updated_user = user_crud.update(db=db, db_obj=db_user, obj_update=user_update)
    return updated_user


@router.get(
    "/coaches/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all coaches",
    response_description="List of all coaches",
)
def get_all_coaches(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_active_user),
) -> Sequence[UserResponse]:
    """Get all users with coach role.

    Args:
        db: The database session. Defaults to Depends(get_db).
        current_user: The current authenticated user. Defaults to Depends(get_current_active_user).

    Returns:
        List of UserResponse objects representing all coaches.
    """
    coaches = user_crud.get_users_by_role(db, RoleName.COACH)
    return coaches
