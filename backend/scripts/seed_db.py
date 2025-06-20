#!/usr/bin/env python3
"""
Script to seed the database with test data.
Run with: python -m scripts.seed_db
"""
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models.user import User, Role, UserRole, RoleName
from src.models.activity import Activity, ActivityBooking
from src.core.security import get_password_hash
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_roles(db: Session):
    """Create user roles if they don't exist."""
    roles_created = []
    for role_name in RoleName:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            logger.info(f"Created role: {role_name}")
            roles_created.append(role)
    if roles_created:
        db.commit()
    return db.query(Role).all()


def create_test_users(db: Session):
    """Create test users with different roles."""
    # First ensure all roles exist
    roles = create_roles(db)
    role_map = {role.name: role for role in roles}

    test_users = [
        {
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "1234567890",
            "password": "Admin@123",  # Must meet password requirements
            "role": RoleName.ADMIN,
        },
        {
            "email": "coach1@example.com",
            "first_name": "Coach",
            "last_name": "One",
            "phone": "1234567891",
            "password": "Coach@123",
            "role": RoleName.COACH,
        },
        {
            "email": "member1@example.com",
            "first_name": "Member",
            "last_name": "One",
            "phone": "1234567892",
            "password": "Member@123",
            "role": RoleName.CLIENT,
        },
        {
            "email": "coach2@example.com",
            "first_name": "Coach",
            "last_name": "Two",
            "phone": "1234567891",
            "password": "Coach@123",
            "role": RoleName.COACH,
        },
    ]

    for user_data in test_users:
        if not db.query(User).filter(User.email == user_data["email"]).first():
            # Hash the password properly
            hashed_password = get_password_hash(user_data["password"])

            # Create user with proper fields
            user = User(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                hashed_password=hashed_password,
            )
            db.add(user)
            db.flush()  # Get the user ID

            # Assign role
            user_role = UserRole(
                user_id=user.id, role_id=role_map[user_data["role"]].id
            )
            db.add(user_role)
            logger.info(f"Created user: {user.email} with role {user_data['role']}")

    db.commit()  # Commit all users and roles at once

    db.commit()
    return db.query(User).all()


def create_test_activities(db: Session, clear_existing: bool = False):
    """Create test activities.

    Args:
        db: Database session
        clear_existing: If True, will delete all existing activities before creating new ones
    """
    from datetime import datetime, timedelta

    if clear_existing:
        # Clear existing activities
        db.query(ActivityBooking).delete()  # Delete bookings first due to foreign key
        db.query(Activity).delete()
        db.commit()
        logger.info("Cleared existing activities and bookings")

    # Get coaches
    coaches = (
        db.query(User)
        .join(UserRole)
        .join(Role)
        .filter(Role.name == RoleName.COACH)
        .all()
    )
    if not coaches:
        logger.warning("No coaches found. Create coaches first.")
        return []

    # Current time rounded to next hour
    now = datetime.now()
    start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    activities = [
        {
            "name": "Morning Yoga",
            "description": "Gentle morning yoga session to start your day",
            "start_time": start_time.replace(hour=8),  # 8 AM
            "duration": 60,
            "credits_required": 1,
            "max_capacity": 15,
        },
        {
            "name": "HIIT Workout",
            "description": "High intensity interval training for all levels",
            "start_time": start_time.replace(hour=12),  # 12 PM
            "duration": 75,
            "credits_required": 2,
            "max_capacity": 10,
        },
        {
            "name": "Evening Pilates",
            "description": "Core strength and stability exercises",
            "start_time": start_time.replace(hour=18),  # 6 PM
            "duration": 90,
            "credits_required": 1,
            "max_capacity": 12,
        },
    ]

    created_activities = []
    for i, activity_data in enumerate(activities):
        # Assign coaches in round-robin fashion
        coach = coaches[i % len(coaches)]

        activity = Activity(
            **activity_data,
            coach_id=coach.id,
        )
        db.add(activity)
        created_activities.append(activity)
        logger.info(
            f"Created activity: {activity.name} with {coach.first_name} {coach.last_name}"
        )

    db.commit()
    return created_activities


def seed_database(clear_existing: bool = False):
    """Main function to seed the database.

    Args:
        clear_existing: If True, will clear existing data before seeding
    """
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")
        create_roles(db)
        create_test_users(db)
        create_test_activities(db, clear_existing=clear_existing)
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed the database with test data")
    parser.add_argument(
        "--clear", action="store_true", help="Clear existing data before seeding"
    )
    args = parser.parse_args()

    if args.clear:
        confirm = input("Are you sure you want to clear existing data? (y/n): ")
        if confirm.lower() != "y":
            print("Aborting...")
            sys.exit(1)

    seed_database(clear_existing=args.clear)
