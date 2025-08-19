from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    cover_letter_id = Column(Integer, ForeignKey("cover_letters.id"), nullable=False)
    status = Column(String, default="applied")
    success_score = Column(Float, default=0.0)
    created = Column(DateTime, default=datetime.utcnow)
    outcome = Column(String, nullable=True)

    # Relationship back to User
    user = relationship("User", back_populates="applications")

