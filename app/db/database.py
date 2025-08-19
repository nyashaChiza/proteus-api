from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# -------------------------
# CONFIGURATION
# -------------------------
DATABASE_URL = config("DATABASE_URL", "sqlite:///./proteus.db")

# For SQLite, check_same_thread must be False
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# -------------------------
# DEPENDENCY
# -------------------------
# FastAPI dependency for endpoints to get DB session
def get_db():
    """
    Provide a database session to FastAPI endpoints.
    Automatically closes session after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
