from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class StockLocation(Base):
    __tablename__ = "stocklocation"
    
    stockid = Column(Integer, primary_key=True, index=True)
    locationid = Column(Integer, ForeignKey("locations.id"), nullable=False)
    stockname = Column(String(100), nullable=False)
    stockdefault = Column(Boolean, default=False)
    
    # Relationships
    location = relationship("Location")
