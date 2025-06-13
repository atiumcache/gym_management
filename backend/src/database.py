from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from src.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recyle=3600,
    echo=settings.debug  # log queries in debug mode
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """
    Database session dependency for FastAPI endpoints.
    Ensures proper cleanup of database connections.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
