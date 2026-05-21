from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import get_current_user, require_admin, get_password_hash, verify_password
from ..models.user import User
from ..schemas.user import UserResponse, UserCreate, ChangePasswordRequest

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return db.query(User).all()

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = User(
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Find the user to update
    db_user = db.query(User).filter(User.userid == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is being changed to an existing email
    if "email" in user_update and user_update["email"] != db_user.email:
        existing_user = db.query(User).filter(User.email == user_update["email"]).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update fields
    if "email" in user_update:
        db_user.email = user_update["email"]
    if "firstname" in user_update:
        db_user.firstname = user_update["firstname"]
    if "lastname" in user_update:
        db_user.lastname = user_update["lastname"]
    if "role" in user_update:
        db_user.role = user_update["role"]
    if "password" in user_update and user_update["password"]:
        db_user.hashed_password = get_password_hash(user_update["password"])
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.userid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting the current user
    if user.userid == current_user.userid:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify current password
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    current_user.hashed_password = get_password_hash(request.new_password)
    current_user.updated_at = __import__('datetime').datetime.utcnow()
    db.commit()
    
    return {"message": "Password changed successfully"}
