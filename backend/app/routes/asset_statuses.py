"""
Asset Statuses API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.asset_status import AssetStatus
from ..schemas.asset_status import AssetStatus as AssetStatusSchema, AssetStatusCreate, AssetStatusUpdate

router = APIRouter(prefix="/asset-statuses", tags=["asset-statuses"])

@router.get("/", response_model=List[AssetStatusSchema])
def get_asset_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all asset statuses"""
    statuses = db.query(AssetStatus).filter(AssetStatus.isactive == True).offset(skip).limit(limit).all()
    return statuses

@router.get("/{status_id}", response_model=AssetStatusSchema)
def get_asset_status(status_id: int, db: Session = Depends(get_db)):
    """Get asset status by ID"""
    status = db.query(AssetStatus).filter(AssetStatus.statusid == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Asset status not found")
    return status

@router.post("/", response_model=AssetStatusSchema)
def create_asset_status(status: AssetStatusCreate, db: Session = Depends(get_db)):
    """Create new asset status"""
    # Check if status code already exists
    existing = db.query(AssetStatus).filter(AssetStatus.statuscode == status.statuscode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Status code already exists")
    
    db_status = AssetStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.put("/{status_id}", response_model=AssetStatusSchema)
def update_asset_status(status_id: int, status: AssetStatusUpdate, db: Session = Depends(get_db)):
    """Update asset status"""
    db_status = db.query(AssetStatus).filter(AssetStatus.statusid == status_id).first()
    if not db_status:
        raise HTTPException(status_code=404, detail="Asset status not found")
    
    for key, value in status.dict(exclude_unset=True).items():
        setattr(db_status, key, value)
    
    db.commit()
    db.refresh(db_status)
    return db_status

@router.delete("/{status_id}")
def delete_asset_status(status_id: int, db: Session = Depends(get_db)):
    """Delete asset status (soft delete)"""
    db_status = db.query(AssetStatus).filter(AssetStatus.statusid == status_id).first()
    if not db_status:
        raise HTTPException(status_code=404, detail="Asset status not found")
    
    db_status.isactive = False
    db.commit()
    return {"message": "Asset status deleted successfully"}
