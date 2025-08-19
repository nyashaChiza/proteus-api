from app.db.database import Base, engine

# Import all models so SQLAlchemy knows about them
from app.models.user import User
from app.models.job import Job
from app.models.application import Application
from app.models.resume import Resume
from app.models.cover_letter import CoverLetter

# Create tables in the database
Base.metadata.create_all(bind=engine)

print("Database initialized successfully!")
