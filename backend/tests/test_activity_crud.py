from datetime import timedelta
import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from src.crud.activity import activity_crud
from src.crud.user import user_crud
from src.models.user import User
from src.schemas.user import UserCreate
from src.models.activity import Activity, ActivityBooking
from src.schemas.activity import ActivityBase, ActivityResponse


class ActivityFactory:
    def __init__(self):
        self.activities_created: int = 0

    def create_activity(self, hour_offset: int = 0, day_offset: int = 0):
        """Create a test activity with configurable start/end times using hour and day offsets.

        Args:
            hour_offset: Hours to add to current time for start_time
            day_offset: Days to add to start_time for end_time

        Returns:
            Activity: A test Activity instance with configured times
        """
        self.activities_created += 1
        start_time = datetime.now() + timedelta(hours=hour_offset, days=day_offset)
        end_time = start_time + timedelta(hours=1)

        return ActivityBase(
            name="Test Activity" + str(self.activities_created),
            description="testing description...",
            coach_id=1,
            start_time=start_time,
            end_time=end_time,
            credits_required=1,
            max_capacity=10,
        )


def test_get_all_activities(test_db: Session):
    """Test retrieving all activities from the database."""
    test_user = UserCreate(
        email="test@example.com",
        password="T@estpassword1!",
        first_name="Test",
        last_name="User",
        phone="14234278012",
    )
    db_user = user_crud.create(db=test_db, obj_create=test_user)
    assert user_crud.set_roles(
        db=test_db, user_id=db_user.id, role_names=["admin", "coach", "client"]
    )
    test_db.refresh(db_user)

    factory = ActivityFactory()
    activity1 = factory.create_activity(hour_offset=1, day_offset=1)
    activity2 = factory.create_activity(hour_offset=2, day_offset=1)

    for activity in [activity1, activity2]:
        activity_crud.create(test_db, activity)

    test_db.commit()

    activities = activity_crud.get_many(test_db)
    assert len(activities) == 2  # There might be other activities in the test DB
