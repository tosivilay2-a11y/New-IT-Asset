"""
Country Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CountryBase(BaseModel):
    countryname: str
    countrycode: str
    isactive: Optional[bool] = True

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseModel):
    countryname: Optional[str] = None
    countrycode: Optional[str] = None
    isactive: Optional[bool] = None

class Country(CountryBase):
    countryid: int
    createdat: Optional[datetime] = None
    updatedat: Optional[datetime] = None
    
    class Config:
        from_attributes = True
