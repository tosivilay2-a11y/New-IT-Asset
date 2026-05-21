"""
Main Categories API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.main_category import MainCategory
from ..schemas.main_category import MainCategory as MainCategorySchema, MainCategoryCreate, MainCategoryUpdate

router = APIRouter(prefix="/main-categories", tags=["main-categories"])

@router.get("/", response_model=List[MainCategorySchema])
def get_main_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all main categories"""
    categories = db.query(MainCategory).filter(MainCategory.isactive == True).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=MainCategorySchema)
def get_main_category(category_id: int, db: Session = Depends(get_db)):
    """Get main category by ID"""
    category = db.query(MainCategory).filter(MainCategory.maincategoryid == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Main category not found")
    return category

@router.post("/", response_model=MainCategorySchema)
def create_main_category(category: MainCategoryCreate, db: Session = Depends(get_db)):
    """Create new main category"""
    # Check if category code already exists
    existing = db.query(MainCategory).filter(MainCategory.categorycode == category.categorycode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category code already exists")
    
    db_category = MainCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=MainCategorySchema)
def update_main_category(category_id: int, category: MainCategoryUpdate, db: Session = Depends(get_db)):
    """Update main category"""
    db_category = db.query(MainCategory).filter(MainCategory.maincategoryid == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Main category not found")
    
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_main_category(category_id: int, db: Session = Depends(get_db)):
    """Delete main category (soft delete)"""
    db_category = db.query(MainCategory).filter(MainCategory.maincategoryid == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Main category not found")
    
    db_category.isactive = False
    db.commit()
    return {"message": "Main category deleted successfully"}
