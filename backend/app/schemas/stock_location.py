from pydantic import BaseModel
from typing import Optional

class StockLocationBase(BaseModel):
    locationid: int
    stockname: str
    stockdefault: Optional[bool] = False

class StockLocationCreate(StockLocationBase):
    pass

class StockLocationUpdate(BaseModel):
    locationid: Optional[int] = None
    stockname: Optional[str] = None
    stockdefault: Optional[bool] = None

class StockLocationResponse(StockLocationBase):
    stockid: int
    
    class Config:
        from_attributes = True
