from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    url = Column(String, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    source = Column(String, nullable=True)  # e.g., LinkedIn, Indeed
    created = Column(DateTime, default=datetime.utcnow)
