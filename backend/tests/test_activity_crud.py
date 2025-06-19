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

    def create_activity(
        self, hour_offset: int = 0, day_offset: int = 0, coach_id: int = 1
    ):
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
            coach_id=coach_id,
            start_time=start_time,
            end_time=end_time,
            credits_required=1,
            max_capacity=10,
        )


class UserFactory:
    def __init__(self):
        self.users_created: int = 0

    def create_user(self, hour_offset: int = 0, day_offset: int = 0, coach_id: int = 1):
        """Create a test activity with configurable start/end times using hour and day offsets.

        Args:
            hour_offset: Hours to add to current time for start_time
            day_offset: Days to add to start_time for end_time

        Returns:
            Activity: A test Activity instance with configured times
        """
        self.users_created += 1
        user_num = str(self.users_created)
        return UserCreate(
            first_name="Test",
            last_name="User" + user_num,
            phone="1234567890" + user_num,
            email="testuser" + user_num + "@gmail.com",
            password="Str@ngPass1!",
        )


def test_get_all_activities(test_db: Session):
    """Test retrieving all activities from the database."""
    u_factory = UserFactory()
    test_user = u_factory.create_user()
    db_user = user_crud.create(db=test_db, obj_create=test_user)

    factory = ActivityFactory()
    activity1 = factory.create_activity(
        hour_offset=1, day_offset=1, coach_id=db_user.id
    )
    activity2 = factory.create_activity(
        hour_offset=2, day_offset=1, coach_id=db_user.id
    )

    for activity in [activity1, activity2]:
        activity_crud.create(test_db, activity)

    test_db.commit()

    activities = activity_crud.get_many(test_db)
    assert len(activities) == 2  # There might be other activities in the test DB


def test_get_activities_by_coach(test_db: Session):
    my_u_factory = UserFactory()
    # Create 5 users
    test_users = [my_u_factory.create_user() for _ in range(5)]
    db_users = [user_crud.create(db=test_db, obj_create=u) for u in test_users]
    # Add all roles to all test users
    coach_ids = []
    for db_u in db_users:
        coach_ids.append(db_u.id)
        assert user_crud.set_roles(
            db=test_db, user_id=db_u.id, role_names=["admin", "coach", "client"]
        )

    my_a_factory = ActivityFactory()
    activity1 = my_a_factory.create_activity(
        hour_offset=1, day_offset=1, coach_id=coach_ids[0]
    )
    activity2 = my_a_factory.create_activity(
        hour_offset=2, day_offset=1, coach_id=coach_ids[1]
    )

    for a in [activity1, activity2]:
        activity_crud.create(db=test_db, obj_create=a)

    test_db.commit()

    activities = activity_crud.get_activities(db=test_db, coach_id=coach_ids[0])
    assert len(activities) == 1
    print(activities[0])
    assert activities[0].coach_id == coach_ids[0]
