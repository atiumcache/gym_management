#!/usr/bin/env python3
"""
Test database management script.

Usage:
    python -m scripts.test_db [command]

Commands:
    create    Create test database
    drop      Drop test database
    reset     Reset test database (drop and recreate)
"""
import sys
import os
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy import create_engine

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test database configuration
TEST_SQLALCHEMY_DATABASE_URL = "postgresql://test:test@localhost:5433/test"

def create_test_db():
    """Create the test database if it doesn't exist."""
    if not database_exists(TEST_SQLALCHEMY_DATABASE_URL):
        print("Creating test database...")
        create_database(TEST_SQLALCHEMY_DATABASE_URL)
        print("Test database created.")
    else:
        print("Test database already exists.")

def drop_test_db():
    """Drop the test database if it exists."""
    if database_exists(TEST_SQLALCHEMY_DATABASE_URL):
        print("Dropping test database...")
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)
        print("Test database dropped.")
    else:
        print("Test database does not exist.")

def reset_test_db():
    """Reset the test database by dropping and recreating it."""
    drop_test_db()
    create_test_db()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify a command: create, drop, or reset")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_test_db()
    elif command == "drop":
        drop_test_db()
    elif command == "reset":
        reset_test_db()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: create, drop, reset")
        sys.exit(1)
