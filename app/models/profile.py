from sqlalchemy import Column, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    base_resume = Column(Text, nullable=True)        # raw markdown string
    base_cover_letter = Column(Text, nullable=True)  # raw markdown string
    preferences = Column(JSON, nullable=True)

    user = relationship("User", back_populates="profile")
