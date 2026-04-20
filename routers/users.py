from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import get_db
from Oauth2 import get_current_user, get_current_admin
import schemas
from utils import verify_password, hash_password    

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model= list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    users = db.query(models.User).all()
    return users
@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user 
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {user_id} not found"
            )
    return user
@router.put("/me", response_model=schemas.UserResponse)
def update_current_user_profile(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if user_update.username:
        existing_user = db.query(models.User).filter(models.User.username == user_update.username, models.User.id != current_user.id).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        current_user.username = user_update.username
    if user_update.email:
        existing_email = db.query(models.User).filter(models.User.email == user_update.email, models.User.id != current_user.id).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        current_user.email = user_update.email
    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)
    db.commit()
    db.refresh(current_user)
    return current_user
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return None
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {user_id} not found"
            )
    db.delete(user)
    db.commit()
    return None