import os
import sys
import time

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import create_database, database_exists

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import settings
from src.database import Base
from src.models.user import Role, User, UserRole

# Test database configuration
TEST_SQLALCHEMY_DATABASE_URL = "postgresql://test:test@localhost:5433/test"


def wait_for_db(engine, max_retries=5, delay_seconds=1):
    """Wait for the database to be available."""
    from sqlalchemy import text
    retries = 0
    while retries < max_retries:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
                return True
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise
            print(f"Database not ready, retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)


@pytest.fixture(scope="session")
def db_engine():
    """Create engine for testing database."""
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    
    # Wait for database to be ready
    wait_for_db(engine)
    
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(db_engine):
    """Create a fresh database for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    
    # Create a session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = TestingSessionLocal()
    
    # Initialize roles
    roles = [Role(name="client"), Role(name="coach"), Role(name="admin")]
    for role in roles:
        db.merge(role)  # Use merge to handle duplicate role creation
    db.commit()
    
    try:
        yield db
    finally:
        # Rollback any changes made during the test
        db.close()
        transaction.rollback()
        connection.close()
