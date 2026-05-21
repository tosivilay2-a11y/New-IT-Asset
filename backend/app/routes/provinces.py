"""
Provinces API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.province import Province
from ..schemas.province import Province as ProvinceSchema, ProvinceCreate, ProvinceUpdate

router = APIRouter(prefix="/provinces", tags=["provinces"])

@router.get("/", response_model=List[ProvinceSchema])
def get_provinces(country_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all provinces, optionally filtered by country"""
    query = db.query(Province).filter(Province.isactive == True)
    
    if country_id:
        query = query.filter(Province.countryid == country_id)
    
    provinces = query.offset(skip).limit(limit).all()
    return provinces

@router.get("/{province_id}", response_model=ProvinceSchema)
def get_province(province_id: int, db: Session = Depends(get_db)):
    """Get province by ID"""
    province = db.query(Province).filter(Province.provinceid == province_id).first()
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    return province

@router.post("/", response_model=ProvinceSchema)
def create_province(province: ProvinceCreate, db: Session = Depends(get_db)):
    """Create new province"""
    db_province = Province(**province.dict())
    db.add(db_province)
    db.commit()
    db.refresh(db_province)
    return db_province

@router.put("/{province_id}", response_model=ProvinceSchema)
def update_province(province_id: int, province: ProvinceUpdate, db: Session = Depends(get_db)):
    """Update province"""
    db_province = db.query(Province).filter(Province.provinceid == province_id).first()
    if not db_province:
        raise HTTPException(status_code=404, detail="Province not found")
    
    for key, value in province.dict(exclude_unset=True).items():
        setattr(db_province, key, value)
    
    db.commit()
    db.refresh(db_province)
    return db_province

@router.delete("/{province_id}")
def delete_province(province_id: int, db: Session = Depends(get_db)):
    """Delete province (soft delete)"""
    db_province = db.query(Province).filter(Province.provinceid == province_id).first()
    if not db_province:
        raise HTTPException(status_code=404, detail="Province not found")
    
    db_province.isactive = False
    db.commit()
    return {"message": "Province deleted successfully"}
