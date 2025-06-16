from src.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func 

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    #roles = relationship('Role', secondary='user_role', back_populates='users')

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Enum('client', 'coach', 'admin')

    #users = relationship('User', secondary='user_role', back_populates='roles')

class UserRole(Base):
    __tablename__ = 'user_role'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)