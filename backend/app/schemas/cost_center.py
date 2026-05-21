"""
Cost Center Schemas — no department link
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CostCenterBase(BaseModel):
    costcentername: str
    costcentercode: str
    countryid: int
    provinceid: Optional[int] = None
    companyid: Optional[int] = None
    description: Optional[str] = None
    isactive: bool = True

class CostCenterCreate(CostCenterBase):
    pass

class CostCenterUpdate(BaseModel):
    costcentername: Optional[str] = None
    costcentercode: Optional[str] = None
    countryid: Optional[int] = None
    provinceid: Optional[int] = None
    companyid: Optional[int] = None
    description: Optional[str] = None
    isactive: Optional[bool] = None

class CostCenter(CostCenterBase):
    costcenterid: int
    createdat: Optional[datetime] = None
    updatedat: Optional[datetime] = None

    class Config:
        from_attributes = True
