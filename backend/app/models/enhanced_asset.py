"""
Enhanced Asset Model - System Configuration Models Only
Note: Country, Province, Company, MainCategory, AssetSequence are defined in separate files
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Date, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class SystemConfig(Base):
    __tablename__ = "systemconfig"
    
    configid = Column(Integer, primary_key=True, index=True)
    configkey = Column(String(100), unique=True, nullable=False)
    configvalue = Column(Text)
    description = Column(String(500))
    category = Column(String(50))
    datatype = Column(String(20), default='string')  # string, number, boolean, json
    isactive = Column(Boolean, default=True)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AssetIDFormat(Base):
    __tablename__ = "assetidformat"
    
    formatid = Column(Integer, primary_key=True, index=True)
    formatname = Column(String(100), nullable=False)
    formatpattern = Column(String(200), nullable=False)
    description = Column(String(500))
    example = Column(String(100))
    isactive = Column(Boolean, default=True)
    isdefault = Column(Boolean, default=False)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
