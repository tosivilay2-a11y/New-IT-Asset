"""
Departments API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.department import Department
from ..schemas.department import Department as DepartmentSchema, DepartmentCreate, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/", response_model=List[DepartmentSchema])
def get_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all departments"""
    departments = db.query(Department).filter(Department.isactive == True).offset(skip).limit(limit).all()
    return departments

@router.get("/company/{company_id}", response_model=List[DepartmentSchema])
def get_departments_by_company(company_id: int, db: Session = Depends(get_db)):
    """Get departments by company"""
    departments = db.query(Department).filter(
        Department.companyid == company_id,
        Department.isactive == True
    ).all()
    return departments

@router.get("/{department_id}", response_model=DepartmentSchema)
def get_department(department_id: int, db: Session = Depends(get_db)):
    """Get department by ID"""
    department = db.query(Department).filter(Department.departmentid == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post("/", response_model=DepartmentSchema)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    """Create new department"""
    # Check if department code already exists
    existing = db.query(Department).filter(Department.departmentcode == department.departmentcode).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department code already exists")
    
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@router.put("/{department_id}", response_model=DepartmentSchema)
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    """Update department"""
    db_department = db.query(Department).filter(Department.departmentid == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department

@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    """Delete department (soft delete)"""
    db_department = db.query(Department).filter(Department.departmentid == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db_department.isactive = False
    db.commit()
    return {"message": "Department deleted successfully"}
