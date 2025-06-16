import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session

from src.main import app
from src.database import get_db
from src.models.user import User, Role, UserRole, RoleName
from src.crud.user import user_crud
from src.schemas.user import UserCreate, UserResponse

# Create a test client that overrides the database dependency
@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_fetch_all_users_empty(client: TestClient, test_db: Session):
    """Test fetching all users when no users exist."""
    response = client.get("/api/v1/user/all")
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
        password="password123",
    )
    user2 = UserCreate(
        email="user2@example.com",
        first_name="User",
        last_name="Two",
        phone="+15303391503",
        password="password123",
    )

    try:
        # Add users to database
        db_user1 = user_crud.create(test_db, user1)
        db_user2 = user_crud.create(test_db, user2)
        test_db.commit()

        # Make request
        response = client.get("/api/v1/user/all")
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
