from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.helpers.security import hash_password
from app.helpers.auth import get_current_user
router = APIRouter(
    tags=["users"]
)

# --------------------------
# CREATE USER
# --------------------------
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_pw,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------------------------
# READ ALL USERS
# --------------------------
@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).offset(skip).limit(limit).all()

# --------------------------
# READ SINGLE USER
# --------------------------
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --------------------------
# UPDATE USER
# --------------------------
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin

    db.commit()
    db.refresh(user)
    return user

# --------------------------
# DELETE USER
# --------------------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db) ,current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return
