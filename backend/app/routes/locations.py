"""
Locations API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models.location import Location
from ..schemas.location import Location as LocationSchema, LocationCreate, LocationUpdate

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/", response_model=List[LocationSchema])
def get_locations(company_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all locations, optionally filtered by company"""
    query = db.query(Location)
    
    if company_id is not None:
        query = query.filter(Location.companyid == company_id)
        
    locations = query.offset(skip).limit(limit).all()
    return locations

@router.get("/{location_id}", response_model=LocationSchema)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Get location by ID"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.post("/", response_model=LocationSchema)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Create new location"""
    # Check if location name already exists
    existing = db.query(Location).filter(Location.name == location.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Location name already exists")
        
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.put("/{location_id}", response_model=LocationSchema)
def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    """Update location"""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
        
    for key, value in location.dict(exclude_unset=True).items():
        setattr(db_location, key, value)
        
    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete location"""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
        
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully"}
