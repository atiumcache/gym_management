from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ActivityBase(BaseModel):
    name: str
    description: str
    coach_id: int
    start_time: datetime
    duration: int
    credits_required: int
    max_capacity: int


class AttendeeInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: PhoneNumber


class ActivityResponse(ActivityBase):
    id: int
    attendees: List[AttendeeInfo]
    coach_first_name: str
    coach_last_name: str
    attendee_count: int
    spots_left: int
