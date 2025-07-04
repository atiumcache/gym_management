import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud.user import user_crud
from src.models.user import Role, RoleName, User, UserRole
from src.schemas.user import UserCreate, UserResponse
from tests.factories import UserFactory, RoleFactory


def test_create_user_success(client: TestClient, test_db: Session):
    """Test creating a new user successfully."""
    user_data = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "phone": "+14155552671",
        "password": "Securepassword123!!",
    }

    response = client.post("/api/v1/user/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["first_name"] == user_data["first_name"]
    assert created_user["last_name"] == user_data["last_name"]
    assert created_user["phone"].replace("-", "") == "14155552671"
    assert "password" not in created_user  # Password should not be returned

    # Verify user exists in database
    db_user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]

    # Clean up
    test_db.delete(db_user)
    test_db.commit()


def test_create_user_duplicate_email(client: TestClient, test_db: Session):
    """Test creating a user with an existing email."""
    # First create a user
    existing_user = UserCreate(
        email="existing@example.com",
        first_name="Existing",
        last_name="User",
        phone="+14155552672",
        password="Password123$!",
    )
    db_user = user_crud.create(test_db, existing_user)
    test_db.commit()

    try:
        # Try to create another user with same email
        duplicate_data = {
            "email": "existing@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone": "+14155552673",
            "password": "Anotherpassword1$!",
        }
        response = client.post("/api/v1/user/", json=duplicate_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    finally:
        # Clean up
        if db_user:
            test_db.delete(db_user)
            test_db.commit()


def test_create_user_invalid_data(client: TestClient, test_db: Session):
    """Test creating a user with invalid data."""
    invalid_data = {
        "email": "not-an-email",  # Invalid email
        "first_name": "",  # Empty first name
        "last_name": "",  # Empty last name
        "phone": "123",  # Invalid phone
        "password": "",  # Empty password
    }

    response = client.post("/api/v1/user/", json=invalid_data)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    )  # Validation error

    errors = response.json()["detail"]
    error_fields = {e["loc"][1] for e in errors}
    assert "email" in error_fields
    assert "first_name" in error_fields
    assert "last_name" in error_fields
    assert "phone" in error_fields
    assert "password" in error_fields


def test_fetch_all_users_empty(client: TestClient, test_db: Session):
    """Test fetching all users when no users exist."""
    response = client.get("/api/v1/users/all")
    assert response.status_code == 200
    assert response.json() == []


def test_fetch_all_users_with_data(client: TestClient, test_db: Session):
    """Test fetching all users when users exist."""
    # Create test users
    user1 = UserCreate(
        email="user1@example.com",
        first_name="User",
        last_name="One",
        phone="+14234278012",
        password="Apassword123@",
    )
    user2 = UserCreate(
        email="user2@example.com",
        first_name="User",
        last_name="Two",
        phone="+15303391503",
        password="Apassword123@",
    )

    try:
        # Add users to database
        db_user1 = user_crud.create(test_db, user1)
        db_user2 = user_crud.create(test_db, user2)
        test_db.commit()

        # Make request
        response = client.get("/api/v1/users/all")
        assert response.status_code == 200

        # Verify response
        users = response.json()
        assert len(users) == 2
        assert any(u["email"] == "user1@example.com" for u in users)
        assert any(u["email"] == "user2@example.com" for u in users)
    finally:
        # Clean up
        if "db_user1" in locals():
            user_crud.delete(test_db, db_user1)
        if "db_user2" in locals():
            user_crud.delete(test_db, db_user2)
        test_db.commit()


def test_user_update(client: TestClient, test_db: Session):
    """Test updating a user record."""
    my_user = UserCreate(
        email="user1@example.com",
        first_name="User",
        last_name="One",
        phone="+14234278012",
        password="Apassword123@",
    )

    try:
        db_user = user_crud.create(test_db, my_user)
        test_db.commit()
        print("PRINTING", db_user.id)
        response = client.get(f"/api/v1/user/{db_user.id}")
        assert response.status_code == 200
        user = response.json()
        assert user["first_name"] == "User"

    finally:
        if "db_user" in locals():
            user_crud.delete(test_db, db_user)
        test_db.commit()


def test_get_coaches(client: TestClient, test_db: Session):
    some_clients = [UserFactory(roles=[RoleFactory(name="client")]) for _ in range(15)]
    test_db.commit()
    num_coaches = 4
    some_coaches = [
        UserFactory(roles=[RoleFactory(name="coach")]) for _ in range(num_coaches)
    ]
    test_db.commit()

    response = client.get("/api/v1/user/coaches/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == num_coaches
