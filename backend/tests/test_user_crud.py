import pytest
from sqlalchemy.orm import Session
from src.models.user import User
from src.crud.user import UserCRUDRepository
from src.schemas.user import UserCreate, UserResponse

@pytest.fixture
def test_user():
    return User(
        email="test@example.com",
        password="hashed_password",
        first_name="Test",
        last_name="User",
        is_active=True
    )

@pytest.fixture
def test_user():
    return User(
        email="test@example.com",
        password="hashed_password",
        first_name="Test",
        last_name="User",
        is_active=True
    )

def test_create_user(test_db: Session):
    # Create the CRUD repository
    user_repo = UserCRUDRepository(User)
    
    # Create a user create schema
    user_create = UserCreate(
        email="newuser@example.com",
        first_name="John",
        last_name="Doe",
        phone="+12345678901",
        password="securepassword123"
    )
    
    # Create the user
    created_user = user_repo.create(test_db, user_create)
    
    # Verify the user was created
    assert created_user is not None
    assert created_user.email == "newuser@example.com"
    assert created_user.first_name == "John"
    assert created_user.last_name == "Doe"
    assert created_user.email == "newuser@example.com"
    assert created_user.first_name == "John"
    assert created_user.last_name == "Doe"
    assert created_user.phone.replace('-', "") == "tel:+12345678901"
    assert created_user.created_at is not None  
    assert created_user.updated_at is not None
    
    # Clean up
    test_db.delete(created_user)
    test_db.commit()

def test_get_user_by_email(test_db: Session):
    # Create the CRUD repository
    user_repo = UserCRUDRepository(User)
    
    # Create a test user using the schema
    user_create = UserCreate(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone="+12345678901",
        password="securepassword123"
    )
    user_repo.create(test_db, user_create)
    
    # Test getting the user by email
    result = user_repo.get_user_by_email(test_db, "test@example.com")
    
    assert result is not None
    assert result.email == "test@example.com"
    assert result.first_name == "Test"
    assert result.last_name == "User"
    assert result.phone.replace("-", "") == "tel:+12345678901"
    assert result.created_at is not None  
    assert result.updated_at is not None
    
    # Test getting a non-existent user
    result = user_repo.get_user_by_email(test_db, "nonexistent@example.com")
    assert result is None

def test_add_role(test_db: Session):
    user_repo = UserCRUDRepository(User)
    
    user_create = UserCreate(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone="+12345678901",
        password="securepassword123"
    )
    
    created_user = user_repo.create(test_db, user_create)
    my_user_id = created_user.id
    add_result = user_repo.add_role(db=test_db, user_id=my_user_id, role_name='admin')
    assert add_result is True
    
    # Get the user after adding role
    my_user = user_repo.get_user_by_email(test_db, 'test@example.com')
    assert my_user is not None
    
    # Check if the user has the admin role
    user_roles = [role.name for role in my_user.roles]
    assert 'admin' in user_roles