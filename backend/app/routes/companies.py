"""
Companies API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.company import Company
from ..schemas.company import Company as CompanySchema, CompanyCreate, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("/", response_model=List[CompanySchema])
def get_companies(province_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all companies, optionally filtered by province"""
    query = db.query(Company).filter(Company.isactive == True)
    
    if province_id:
        query = query.filter(Company.provinceid == province_id)
    
    companies = query.offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=CompanySchema)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company by ID"""
    company = db.query(Company).filter(Company.companyid == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/", response_model=CompanySchema)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create new company"""
    # Check if company code already exists
    existing = db.query(Company).filter(Company.companycode == company.companycode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company code already exists")
    
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.put("/{company_id}", response_model=CompanySchema)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    """Update company"""
    db_company = db.query(Company).filter(Company.companyid == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete company (soft delete)"""
    db_company = db.query(Company).filter(Company.companyid == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_company.isactive = False
    db.commit()
    return {"message": "Company deleted successfully"}
