import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer
from pydantic_extra_types.phone_numbers import PhoneNumber
from phonenumbers import parse, is_valid_number, NumberParseException


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=10, max_length=15)

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        # TODO: Implement standardized validation from PhoneNumber library
        # Remove all non-digit characters
        digits = "".join(c for c in v if c.isdigit())

        # Check if we have between 10-15 digits (standard phone number lengths with/without country code)
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Phone number must be 10-15 digits")

        return digits  # Return just the digits for consistent storage


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="""
        Password must be at least 8 characters long and contain:
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character (@$!%*?&)
        """,
    )

    @field_validator("password")
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError(
                "Password must contain at least one special character (@$!%*?&)"
            )
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserBase):
    id: int
    email: EmailStr  # Required
    first_name: str  # Required
    last_name: str  # Required
    phone: str = Field(..., min_length=10, max_length=15)


class UserPasswordUpdate(UserBase):
    # TODO
    pass
