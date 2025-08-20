from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProfileBase(BaseModel):
    base_resume: Optional[str] = None
    base_cover_letter: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
