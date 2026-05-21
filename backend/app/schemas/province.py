"""
Province Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProvinceBase(BaseModel):
    provincename: str
    provincecode: str
    countryid: int
    isactive: Optional[bool] = True

class ProvinceCreate(ProvinceBase):
    pass

class ProvinceUpdate(BaseModel):
    provincename: Optional[str] = None
    provincecode: Optional[str] = None
    countryid: Optional[int] = None
    isactive: Optional[bool] = None

class Province(ProvinceBase):
    provinceid: int
    createdat: Optional[datetime] = None
    updatedat: Optional[datetime] = None
    
    class Config:
        from_attributes = True
