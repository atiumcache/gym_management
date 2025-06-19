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
from tests.factories import ActivityFactory, UserFactory, RoleFactory


def test_filtered_route(test_db: Session, client):
    # Create 2 coaches
    coach1, coach2 = [UserFactory(roles=[RoleFactory(name="coach")]) for _ in range(2)]
    test_db.commit()

    # Create activities
    num_coach1 = 10
    num_coach2 = 15
    activities_coach1 = [ActivityFactory(coach=coach1) for _ in range(num_coach1)]
    activities_coach2 = [ActivityFactory(coach=coach2) for _ in range(num_coach2)]

    response = client.get(
        f"/api/v1/activity/filtered?coach_id={coach1.id}&include_past=True"
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data) == num_coach1
    assert all(activity["coach_id"] == coach1.id for activity in data)
