import sys
import os
import pytest

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.config import settings
from src.models.user import Role


@pytest.fixture(scope="function")
def test_db():
    """Fixture for creating a fresh in-memory SQLite database for each test."""
    engine = create_engine("sqlite://")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()

    # Initialize roles
    roles = [Role(name="client"), Role(name="coach"), Role(name="admin")]
    db.add_all(roles)
    db.commit()

    try:
        yield db
    finally:
        # Clean up
        db.close()
        Base.metadata.drop_all(bind=engine)
