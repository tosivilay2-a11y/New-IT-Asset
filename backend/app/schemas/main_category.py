"""
Main Category Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MainCategoryBase(BaseModel):
    categoryname: str
    categorycode: str
    description: Optional[str] = None
    isactive: Optional[bool] = True

class MainCategoryCreate(MainCategoryBase):
    pass

class MainCategoryUpdate(BaseModel):
    categoryname: Optional[str] = None
    categorycode: Optional[str] = None
    description: Optional[str] = None
    isactive: Optional[bool] = None

class MainCategory(MainCategoryBase):
    maincategoryid: int
    createdat: Optional[datetime] = None
    updatedat: Optional[datetime] = None
    
    class Config:
        from_attributes = True
