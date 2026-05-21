"""
Cost Centers API Routes
Full CRUD with filtering support by country/province/company/department
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models.cost_center import CostCenter
from ..schemas.cost_center import CostCenter as CostCenterSchema, CostCenterCreate, CostCenterUpdate

router = APIRouter(prefix="/cost-centers", tags=["cost-centers"])


@router.get("/", response_model=List[CostCenterSchema])
def get_cost_centers(
    skip: int = 0,
    limit: int = 200,
    country_id: Optional[int] = None,
    province_id: Optional[int] = None,
    company_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all active cost centers with optional filters"""
    query = db.query(CostCenter).filter(CostCenter.isactive == True)
    if country_id:
        query = query.filter(CostCenter.countryid == country_id)
    if province_id:
        query = query.filter(CostCenter.provinceid == province_id)
    if company_id:
        query = query.filter(CostCenter.companyid == company_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{cost_center_id}", response_model=CostCenterSchema)
def get_cost_center(cost_center_id: int, db: Session = Depends(get_db)):
    """Get a single cost center by ID"""
    cc = db.query(CostCenter).filter(CostCenter.costcenterid == cost_center_id).first()
    if not cc:
        raise HTTPException(status_code=404, detail="Cost center not found")
    return cc


@router.post("/", response_model=CostCenterSchema)
def create_cost_center(cost_center: CostCenterCreate, db: Session = Depends(get_db)):
    """Create a new cost center"""
    existing = db.query(CostCenter).filter(CostCenter.costcentercode == cost_center.costcentercode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cost center code already exists")
    db_cc = CostCenter(**cost_center.dict())
    db.add(db_cc)
    db.commit()
    db.refresh(db_cc)
    return db_cc


@router.put("/{cost_center_id}", response_model=CostCenterSchema)
def update_cost_center(cost_center_id: int, cost_center: CostCenterUpdate, db: Session = Depends(get_db)):
    """Update an existing cost center"""
    db_cc = db.query(CostCenter).filter(CostCenter.costcenterid == cost_center_id).first()
    if not db_cc:
        raise HTTPException(status_code=404, detail="Cost center not found")
    for key, value in cost_center.dict(exclude_unset=True).items():
        setattr(db_cc, key, value)
    db.commit()
    db.refresh(db_cc)
    return db_cc


@router.delete("/{cost_center_id}")
def delete_cost_center(cost_center_id: int, db: Session = Depends(get_db)):
    """Soft-delete a cost center"""
    db_cc = db.query(CostCenter).filter(CostCenter.costcenterid == cost_center_id).first()
    if not db_cc:
        raise HTTPException(status_code=404, detail="Cost center not found")
    db_cc.isactive = False
    db.commit()
    return {"message": "Cost center deleted successfully"}
