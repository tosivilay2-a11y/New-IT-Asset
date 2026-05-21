"""
Department Schemas — now includes costcenterid
"""
from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    departmentname: str
    departmentcode: str
    companyid: int
    countryid: Optional[int] = None
    provinceid: Optional[int] = None
    costcenterid: Optional[int] = None
    description: Optional[str] = None
    isactive: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    departmentname: Optional[str] = None
    departmentcode: Optional[str] = None
    companyid: Optional[int] = None
    countryid: Optional[int] = None
    provinceid: Optional[int] = None
    costcenterid: Optional[int] = None
    description: Optional[str] = None
    isactive: Optional[bool] = None

class Department(DepartmentBase):
    departmentid: int
    
    class Config:
        from_attributes = True
