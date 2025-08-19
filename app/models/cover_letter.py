from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=True)
    file_path = Column(String, nullable=False)  # e.g., "covers/cover_123.pdf"
    created = Column(DateTime, default=datetime.utcnow)
