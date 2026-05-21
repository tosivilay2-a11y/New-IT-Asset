"""
Main Category Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class MainCategory(Base):
    __tablename__ = "maincategories"
    
    maincategoryid = Column(Integer, primary_key=True, index=True)
    categoryname = Column(String(100), unique=True, nullable=False)
    categorycode = Column(String(1), unique=True, nullable=False)  # 1-char code (e.g., C=Computer, M=Monitor, W=Workstation)
    description = Column(String(500))
    isactive = Column(Boolean, default=True)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assets = relationship("Asset", back_populates="main_category")
