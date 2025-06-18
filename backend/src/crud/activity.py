from datetime import datetime, date
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import and_, or_

from src.crud.base import CRUDRepository
from src.models.activity import Activity, ActivityBooking
from src.models.user import User


class ActivityCRUDRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Activity)

    def get_activities(
        self,
        db: Session,
        coach_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        min_available_spots: Optional[int] = None,
        include_past: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve activities with optional filtering.

        Args:
            db: Database session
            coach_id: Filter by coach ID
            start_date: Filter activities after this date
            end_date: Filter activities before this date
            min_available_spots: Filter activities with at least this many spots available
            include_past: Whether to include past activities (default: False)

        Returns:
            List of activities with attendee information
        """
        # Start building the query
        query = db.query(Activity)

        # Apply filters
        if coach_id is not None:
            query = query.filter(Activity.coach_id == coach_id)

        if start_date:
            query = query.filter(
                Activity.start_time >= datetime.combine(start_date, datetime.min.time())
            )

        if end_date:
            query = query.filter(
                Activity.start_time <= datetime.combine(end_date, datetime.max.time())
            )

        if not include_past:
            query = query.filter(Activity.start_time >= datetime.now())

        # Load related data
        query = query.options(
            joinedload(Activity.coach).load_only(
                User.first_name, User.last_name, User.email, User.phone_number
            ),
            joinedload(Activity.bookings)
            .joinedload(ActivityBooking.user)
            .load_only(User.first_name, User.last_name, User.email, User.phone_number),
        )

        # Execute query
        activities = query.order_by(Activity.start_time).all()

        # Process results
        result = []
        for activity in activities:
            # Calculate available spots
            booked_count = len(
                [b for b in activity.bookings if b.booking_status == "confirmed"]
            )
            available_spots = activity.max_capacity - booked_count

            # Skip if not enough available spots
            if (
                min_available_spots is not None
                and available_spots < min_available_spots
            ):
                continue

            # Prepare attendee information
            attendees = [
                {
                    "id": booking.user.id,
                    "first_name": booking.user.first_name,
                    "last_name": booking.user.last_name,
                    "email": booking.user.email,
                    "phone": booking.user.phone_number,
                    "booking_status": booking.booking_status,
                    "credits_used": booking.credits_used,
                }
                for booking in activity.bookings
            ]

            result.append(
                {
                    "id": activity.id,
                    "coach_id": activity.coach_id,
                    "coach_first_name": activity.coach.first_name,
                    "coach_last_name": activity.coach.last_name,
                    "start_time": activity.start_time,
                    "end_time": activity.end_time,
                    "credits_required": activity.credits_required,
                    "max_capacity": activity.max_capacity,
                    "available_spots": available_spots,
                    "attendees": attendees,
                    "attendee_count": booked_count,
                }
            )

        return result


activity_crud = ActivityCRUDRepository()
