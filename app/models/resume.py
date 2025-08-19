from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=True)  # Optional: which job this resume was tailored for
    file_path = Column(String, nullable=False)  # e.g., "resumes/resume_123.pdf"
    created = Column(DateTime, default=datetime.utcnow)
