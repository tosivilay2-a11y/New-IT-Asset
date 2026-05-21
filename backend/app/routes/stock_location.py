from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.stock_location import StockLocation
from ..models.system_config import SystemConfig
from ..models.user import User
from ..schemas.stock_location import (
    StockLocationCreate, StockLocationUpdate, StockLocationResponse
)

router = APIRouter(prefix="/stock-locations", tags=["stock-locations"])

@router.get("/", response_model=List[StockLocationResponse])
def list_stock_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all stock locations"""
    stock_locations = db.query(StockLocation).all()
    return stock_locations

@router.post("/set-default/{stock_id}")
def set_default_stock_location(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Set a stock location as default and unset others"""
    # Find the stock location to set as default
    stock_location = db.query(StockLocation).filter(
        StockLocation.stockid == stock_id
    ).first()
    
    if not stock_location:
        raise HTTPException(status_code=404, detail="Stock location not found")
    
    # Set all other stock locations to not default
    db.query(StockLocation).filter(
        StockLocation.stockid != stock_id
    ).update({StockLocation.stockdefault: False}, synchronize_session=False)
    
    # Set this one as default
    stock_location.stockdefault = True
    db.add(stock_location)
    
    db.commit()
    db.refresh(stock_location)
    
    return {
        "message": f"Stock location '{stock_location.stockname}' set as default",
        "stock_location": stock_location
    }

@router.get("/config/current")
def get_current_stock_location(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the currently configured stock location"""
    config = db.query(SystemConfig).filter(
        SystemConfig.config_key == 'stock_location'
    ).first()
    
    if not config or not config.config_value:
        return {"stockid": None, "stockname": None, "locationid": None}
    
    try:
        stock_id = int(config.config_value)
        stock_location = db.query(StockLocation).filter(
            StockLocation.stockid == stock_id
        ).first()
        
        if stock_location:
            return {
                "stockid": stock_location.stockid,
                "stockname": stock_location.stockname,
                "locationid": stock_location.locationid
            }
    except (ValueError, TypeError):
        pass
    
    return {"stockid": None, "stockname": None, "locationid": None}

@router.get("/{stock_id}", response_model=StockLocationResponse)
def get_stock_location(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get stock location by ID"""
    stock_location = db.query(StockLocation).filter(
        StockLocation.stockid == stock_id
    ).first()
    
    if not stock_location:
        raise HTTPException(status_code=404, detail="Stock location not found")
    
    return stock_location

@router.post("/", response_model=StockLocationResponse)
def create_stock_location(
    stock_location: StockLocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new stock location"""
    db_stock_location = StockLocation(**stock_location.dict())
    db.add(db_stock_location)
    db.commit()
    db.refresh(db_stock_location)
    return db_stock_location

@router.put("/{stock_id}", response_model=StockLocationResponse)
def update_stock_location(
    stock_id: int,
    stock_location: StockLocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update stock location"""
    db_stock_location = db.query(StockLocation).filter(
        StockLocation.stockid == stock_id
    ).first()
    
    if not db_stock_location:
        raise HTTPException(status_code=404, detail="Stock location not found")
    
    for key, value in stock_location.dict(exclude_unset=True).items():
        setattr(db_stock_location, key, value)
    
    db.commit()
    db.refresh(db_stock_location)
    return db_stock_location

@router.delete("/{stock_id}")
def delete_stock_location(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete stock location"""
    db_stock_location = db.query(StockLocation).filter(
        StockLocation.stockid == stock_id
    ).first()
    
    if not db_stock_location:
        raise HTTPException(status_code=404, detail="Stock location not found")
    
    db.delete(db_stock_location)
    db.commit()
    return {"message": "Stock location deleted successfully"}