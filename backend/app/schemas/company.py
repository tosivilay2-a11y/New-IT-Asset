"""
Company Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CompanyBase(BaseModel):
    companyname: str
    companycode: str
    provinceid: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    isactive: Optional[bool] = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    companyname: Optional[str] = None
    companycode: Optional[str] = None
    provinceid: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    isactive: Optional[bool] = None

class Company(CompanyBase):
    companyid: int
    createdat: Optional[datetime] = None
    updatedat: Optional[datetime] = None
    
    class Config:
        from_attributes = True
