from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut
from app.helpers.auth import get_current_user 

router = APIRouter(tags=["profiles"])

@router.post("/", response_model=ProfileOut)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    existing = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    db_profile = models.Profile(**profile.dict(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/me", response_model=ProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/me", response_model=ProfileOut)
def update_my_profile(
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

@router.put("/{profile_id}", response_model=ProfileOut)
def update_profile(
    profile_id: int,
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id, models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found or not yours")

    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

