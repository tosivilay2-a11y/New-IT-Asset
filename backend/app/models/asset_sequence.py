"""
Asset Sequence Model - Tracks sequence numbers for asset ID generation
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from ..core.database import Base

class AssetSequence(Base):
    __tablename__ = "assetsequences"
    
    sequenceid = Column(Integer, primary_key=True, index=True)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=False)
    companyid = Column(Integer, ForeignKey("companies.companyid"), nullable=False)
    sequenceyear = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    lastsequence = Column(Integer, default=0)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ensure unique sequence per country+company+year
    __table_args__ = (
        UniqueConstraint('countryid', 'companyid', 'sequenceyear', name='uq_country_company_year'),
    )
