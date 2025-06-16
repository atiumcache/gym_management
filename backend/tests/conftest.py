import sys
import os
import pytest

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.config import settings


@pytest.fixture(scope="function")
def test_db():
    """Fixture for creating a fresh in-memory SQLite database for each test."""
    # Create a fresh in-memory SQLite database
    engine = create_engine("sqlite://")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        # Clean up
        db.close()
        Base.metadata.drop_all(bind=engine)
