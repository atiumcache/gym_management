from sqlalchemy import Column, Enum, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import relationship

from src.models.user import User
from enum import Enum as PyEnum

from src.database import Base


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    description = Column(Text)
    coach_id = Column(Integer, ForeignKey("user.id"))
    coach = relationship("User", back_populates="coached_activities")
    start_time = Column(DateTime)
    duration = Column(Integer)
    # required_credit_type_id = Column(Integer) # TODO: add foreign key
    credits_required = Column(Integer)
    max_capacity = Column(Integer)
    # recurring? TODO
    bookings = relationship(
        "ActivityBooking", back_populates="activity", cascade="all, delete-orphan"
    )


class BookingStatus(str, PyEnum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLIST = "waitlist"


class ActivityBooking(Base):
    __tablename__ = "activity_booking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    activity_id = Column(Integer, ForeignKey("activity.id"))
    activity = relationship("Activity", back_populates="bookings")
    user = relationship("User", back_populates="activity_bookings")
    credits_used = Column(Integer)
    booking_status = Column(Enum(BookingStatus, name="activity_booking_status"))
