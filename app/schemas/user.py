from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
