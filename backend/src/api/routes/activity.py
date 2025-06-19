from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_active_user
from src.crud.activity import activity_crud
from src.database import get_db
from src.models.user import User

router = APIRouter()


# View current bookings for a specific client (and/or for 'me', as a client viewing their own bookings)


@router.get("/filtered")
async def get_activities(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_active_user),
    coach_id: Optional[int] = Query(None, description="Filter by coach ID"),
    start_date: Optional[date] = Query(
        None, description="Filter activities after this date (YYYY-MM-DD)"
    ),
    end_date: Optional[date] = Query(
        None, description="Filter activities before this date (YYYY-MM-DD)"
    ),
    min_available_spots: Optional[int] = Query(
        None,
        ge=0,
        description="Filter activities with at least this many spots available",
    ),
    include_past: bool = Query(False, description="Whether to include past activities"),
):
    """
    Retrieve activities with optional filtering.

    Available filters:
    - coach_id: Filter by coach
    - start_date: Only show activities after this date
    - end_date: Only show activities before this date
    - min_available_spots: Only show activities with at least this many spots available
    - include_past: Whether to include past activities (default: False)
    """
    try:
        activities = activity_crud.get_activities(
            db=db,
            coach_id=coach_id,
            start_date=start_date,
            end_date=end_date,
            min_available_spots=min_available_spots,
            include_past=include_past,
        )
        return activities
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving activities: {str(e)}"
        )
