from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    roles = relationship("Role", secondary="user_role", back_populates="users")
    coached_activities = relationship("Activity", back_populates="coach")
    activity_bookings = relationship("ActivityBooking", back_populates="user")


class RoleName(str, PyEnum):
    CLIENT = "client"
    COACH = "coach"
    ADMIN = "admin"


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(RoleName, name="role_name"))

    users = relationship("User", secondary="user_role", back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)
