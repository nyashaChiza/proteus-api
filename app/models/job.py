from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending") #.e.g pending,applied
    url = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=True)  # e.g., LinkedIn, Indeed
    created = Column(DateTime, default=datetime.utcnow)
