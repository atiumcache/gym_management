from database import Base
from sqlalchemy import Column, Timestamp, Integer, Enum, ForeignKey


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coach_id = Column(Integer, ForeignKey("user.id"))
    start_time = Column(Timestamp)
    end_time = Column(Timestamp)
    # required_credit_type_id = Column(Integer) # TODO: add foreign key
    credits_required = Column(Integer)
    max_capacity = Column(Integer)
    # recurring? TODO


class ActivityBooking(Base):
    __tablename__ = "activity_booking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    activity_id = Column(Integer, ForeignKey("activity.id"))
    credits_used = Column(Integer)
    booking_status = Column(Enum("confirmed", "cancelled", "waitlist"))
