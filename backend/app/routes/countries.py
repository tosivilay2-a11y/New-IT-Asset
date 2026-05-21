"""
Countries API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.country import Country
from ..schemas.country import Country as CountrySchema, CountryCreate, CountryUpdate

router = APIRouter(prefix="/countries", tags=["countries"])

@router.get("/", response_model=List[CountrySchema])
def get_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all countries"""
    countries = db.query(Country).filter(Country.isactive == True).offset(skip).limit(limit).all()
    return countries

@router.get("/{country_id}", response_model=CountrySchema)
def get_country(country_id: int, db: Session = Depends(get_db)):
    """Get country by ID"""
    country = db.query(Country).filter(Country.countryid == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.post("/", response_model=CountrySchema)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    """Create new country"""
    # Check if country code already exists
    existing = db.query(Country).filter(Country.countrycode == country.countrycode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Country code already exists")
    
    db_country = Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

@router.put("/{country_id}", response_model=CountrySchema)
def update_country(country_id: int, country: CountryUpdate, db: Session = Depends(get_db)):
    """Update country"""
    db_country = db.query(Country).filter(Country.countryid == country_id).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    for key, value in country.dict(exclude_unset=True).items():
        setattr(db_country, key, value)
    
    db.commit()
    db.refresh(db_country)
    return db_country

@router.delete("/{country_id}")
def delete_country(country_id: int, db: Session = Depends(get_db)):
    """Delete country (soft delete)"""
    db_country = db.query(Country).filter(Country.countryid == country_id).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    db_country.isactive = False
    db.commit()
    return {"message": "Country deleted successfully"}
