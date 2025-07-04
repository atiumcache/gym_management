import os
import sys
import time

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import create_database, database_exists

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import settings
from src.database import Base, get_db
from src.models.user import Role, User, UserRole
from src.models.activity import Activity, ActivityBooking
from fastapi.testclient import TestClient
from fastapi import Depends
from src.main import app

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
            print(
                f"Database not ready, retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay_seconds)


@pytest.fixture(scope="session")
def db_engine():
    """Create engine for testing database."""
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        poolclass=StaticPool,
    )

    # Wait for database to be ready
    wait_for_db(engine)

    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)

    # Drop all tables first to ensure clean state
    Base.metadata.drop_all(bind=engine)

    # Create public schema if it doesn't exist
    from sqlalchemy.schema import CreateSchema, MetaData

    with engine.connect() as conn:
        if not conn.dialect.has_schema(conn, "public"):
            conn.execute(CreateSchema("public"))
        conn.commit()

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Reflect the database to see what tables exist
    meta = MetaData()
    meta.reflect(bind=engine)
    if not meta.tables:
        print("WARNING: No tables found in database after creation!")

    yield engine

    # Clean up
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(db_engine):
    """Create a fresh database session for each test with a clean state."""
    # Create a new connection and transaction
    connection = db_engine.connect()
    transaction = connection.begin()

    # Create a session bound to our connection
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=connection
    )
    db = TestingSessionLocal()

    # Set the session for all factories
    from tests.factories import set_sqlalchemy_session

    set_sqlalchemy_session(db)

    # Initialize required roles
    try:
        # Clear all data first
        db.query(UserRole).delete()
        db.query(User).delete()
        db.query(Role).delete()

        # Add required roles
        roles = [Role(name="client"), Role(name="coach"), Role(name="admin")]
        db.add_all(roles)
        db.commit()

        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        # Clean up
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(test_db):
    """Test client that uses the test_db session."""

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
