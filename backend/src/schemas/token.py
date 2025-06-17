from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""

    email: EmailStr | None = None
    scopes: list[str] = []


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str
