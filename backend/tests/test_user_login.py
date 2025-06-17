import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import verify_password

client = TestClient(app)


def test_register_user_success(test_db: Session):
    """Test successful user registration."""
    user_data = {
        "email": "test@example.com",
        "password": "Str0ngP@ssword1!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+19234567890",
    }

    response = client.post("/api/v1/user", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Verify user data in response
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert "password" not in data  # Password should never be in response

    # Verify user in database
    db_user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert verify_password(user_data["password"], db_user.hashed_password)


def test_register_duplicate_email(test_db: Session):
    """Test registration with duplicate email fails."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "Str0ngP@ssword!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+19234567890",
    }

    # First registration should succeed
    response = client.post("/api/v1/user", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Second registration with same email should fail
    response = client.post("/api/v1/user/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(test_db: Session):
    """Test successful login returns access token."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "password": "Str0ngP@ssword1!",
        "first_name": "Login",
        "last_name": "Test",
        "phone": "+11234567890",
    }
    client.post("/api/v1/user/", json=user_data)

    # Test login
    login_data = {"username": user_data["email"], "password": user_data["password"]}

    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(test_db: Session):
    """Test login with wrong password is rejected."""
    # Register a user
    user_data = {
        "email": "login2@example.com",
        "password": "Str0ngP@ssword!",
        "first_name": "Login",
        "last_name": "Test",
        "phone": "+11234567890",
    }
    client.post("/api/v1/user/", json=user_data)

    # Test login with wrong password
    login_data = {"username": user_data["email"], "password": "wrongpassword"}

    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect email or password" in response.json()["detail"].lower()


def test_protected_route_with_valid_token(test_db: Session):
    """Test accessing a protected route with a valid token."""
    # Register and login
    user_data = {
        "email": "protected@example.com",
        "password": "Str0ngP@ssword!",
        "first_name": "Protected",
        "last_name": "Route",
        "phone": "+19234567890",
    }
    client.post("/api/v1/user", json=user_data)

    login_data = {"username": user_data["email"], "password": user_data["password"]}

    # Get token
    response = client.post("/api/v1/auth/token", data=login_data)
    token = response.json()["access_token"]

    # Access protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/user/me", headers=headers)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user_data["email"]


def test_protected_route_without_token():
    """Test accessing a protected route without a token is rejected."""
    response = client.get("/api/v1/user/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "not authenticated" in response.json()["detail"].lower()
