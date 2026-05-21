"""
Admin Routes - System Configuration and Asset ID Management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.enhanced_asset import SystemConfig, AssetIDFormat
from ..models.asset_sequence import AssetSequence
from ..services.asset_id_generator import AssetIDGenerator
from pydantic import BaseModel
import json

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Pydantic Schemas
class SystemConfigCreate(BaseModel):
    configkey: str
    configvalue: str
    description: Optional[str] = None
    category: Optional[str] = None
    datatype: str = "string"

class SystemConfigUpdate(BaseModel):
    configvalue: str
    description: Optional[str] = None

class AssetIDFormatCreate(BaseModel):
    formatname: str
    formatpattern: str
    description: Optional[str] = None
    example: Optional[str] = None
    isdefault: bool = False

def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin role"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# =============================================
# SYSTEM CONFIGURATION
# =============================================

@router.get("/config")
async def list_system_configs(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all system configurations"""
    
    query = db.query(SystemConfig)
    
    if category:
        query = query.filter(SystemConfig.category == category)
    
    configs = query.all()
    
    return {
        "total": len(configs),
        "data": [
            {
                "configid": c.configid,
                "configkey": c.configkey,
                "configvalue": c.configvalue,
                "description": c.description,
                "category": c.category,
                "datatype": c.datatype,
                "isactive": c.isactive
            }
            for c in configs
        ]
    }

@router.post("/config")
async def create_system_config(
    config_data: SystemConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new system configuration"""
    
    # Check if key already exists
    existing = db.query(SystemConfig).filter(
        SystemConfig.configkey == config_data.configkey
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Configuration key already exists")
    
    new_config = SystemConfig(
        configkey=config_data.configkey,
        configvalue=config_data.configvalue,
        description=config_data.description,
        category=config_data.category,
        datatype=config_data.datatype,
        isactive=1,  # Use 1 for true (integer, not boolean)
        createdat=datetime.utcnow(),
        updatedat=datetime.utcnow()
    )
    
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    
    return {
        "success": True,
        "message": "Configuration created successfully",
        "data": {
            "configid": new_config.configid,
            "configkey": new_config.configkey
        }
    }

@router.put("/config/{config_key}")
async def update_system_config(
    config_key: str,
    config_data: SystemConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update system configuration"""
    
    config = db.query(SystemConfig).filter(
        SystemConfig.configkey == config_key
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config.configvalue = config_data.configvalue
    if config_data.description:
        config.description = config_data.description
    config.updatedat = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Configuration updated successfully"
    }

@router.get("/config/{config_key}")
async def get_system_config(
    config_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get specific system configuration"""
    
    config = db.query(SystemConfig).filter(
        SystemConfig.configkey == config_key
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return {
        "configid": config.configid,
        "configkey": config.configkey,
        "configvalue": config.configvalue,
        "description": config.description,
        "category": config.category,
        "datatype": config.datatype,
        "isactive": config.isactive
    }

# =============================================
# ASSET ID FORMAT MANAGEMENT
# =============================================

@router.get("/asset-id-formats")
async def list_asset_id_formats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all asset ID formats"""
    
    formats = db.query(AssetIDFormat).all()
    
    return {
        "total": len(formats),
        "data": [
            {
                "formatid": f.formatid,
                "formatname": f.formatname,
                "formatpattern": f.formatpattern,
                "description": f.description,
                "example": f.example,
                "isactive": f.isactive,
                "isdefault": f.isdefault
            }
            for f in formats
        ]
    }

@router.post("/asset-id-formats")
async def create_asset_id_format(
    format_data: AssetIDFormatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new asset ID format"""
    
    # If setting as default, unset other defaults
    if format_data.isdefault:
        db.query(AssetIDFormat).update({"isdefault": False})
    
    new_format = AssetIDFormat(
        formatname=format_data.formatname,
        formatpattern=format_data.formatpattern,
        description=format_data.description,
        example=format_data.example,
        isactive=1,  # Use 1 for true (integer, not boolean)
        isdefault=format_data.isdefault,
        createdat=datetime.utcnow(),
        updatedat=datetime.utcnow()
    )
    
    db.add(new_format)
    db.commit()
    db.refresh(new_format)
    
    return {
        "success": True,
        "message": "Asset ID format created successfully",
        "data": {
            "formatid": new_format.formatid,
            "formatname": new_format.formatname
        }
    }

@router.put("/asset-id-formats/{format_id}/set-default")
async def set_default_format(
    format_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Set asset ID format as default"""
    
    # Unset all defaults
    db.query(AssetIDFormat).update({"isdefault": False})
    
    # Set new default
    format_obj = db.query(AssetIDFormat).filter(
        AssetIDFormat.formatid == format_id
    ).first()
    
    if not format_obj:
        raise HTTPException(status_code=404, detail="Format not found")
    
    format_obj.isdefault = True
    format_obj.updatedat = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Default format updated successfully"
    }

# =============================================
# ASSET SEQUENCE MANAGEMENT
# =============================================

@router.get("/asset-sequences")
async def list_asset_sequences(
    country_id: Optional[int] = None,
    company_id: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all asset sequences"""
    
    query = db.query(AssetSequence)
    
    if country_id:
        query = query.filter(AssetSequence.countryid == country_id)
    if company_id:
        query = query.filter(AssetSequence.companyid == company_id)
    if year:
        query = query.filter(AssetSequence.sequenceyear == year)
    
    sequences = query.all()
    
    return {
        "total": len(sequences),
        "data": [
            {
                "sequenceid": s.sequenceid,
                "countryid": s.countryid,
                "companyid": s.companyid,
                "year": s.year,
                "lastsequence": s.lastsequence,
                "updatedat": s.updatedat
            }
            for s in sequences
        ]
    }

@router.post("/asset-sequences/reset")
async def reset_asset_sequence(
    country_id: int,
    company_id: int,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Reset asset sequence (DANGEROUS - Admin only)"""
    
    success = AssetIDGenerator.reset_sequence(db, country_id, company_id, year)
    
    if not success:
        raise HTTPException(status_code=404, detail="Sequence not found")
    
    return {
        "success": True,
        "message": "Sequence reset successfully",
        "warning": "All future assets will start from sequence 0001"
    }

@router.get("/asset-sequences/next")
async def get_next_sequence(
    country_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get next sequence number without incrementing"""
    
    next_seq = AssetIDGenerator.get_next_sequence(db, country_id, company_id)
    
    return {
        "country_id": country_id,
        "company_id": company_id,
        "year": datetime.now().year,
        "next_sequence": next_seq
    }

# =============================================
# SYSTEM STATISTICS
# =============================================

@router.get("/statistics")
async def get_system_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get system-wide statistics"""
    
    from ..models.asset import Asset
    from ..models.country import Country
    from ..models.company import Company
    
    total_assets = db.query(Asset).count()
    total_countries = db.query(Country).filter(Country.isactive == True).count()
    total_companies = db.query(Company).filter(Company.isactive == True).count()
    
    # Assets by status
    from sqlalchemy import func
    status_counts = db.query(
        Asset.status,
        func.count(Asset.assetid)
    ).group_by(Asset.status).all()
    
    return {
        "total_assets": total_assets,
        "total_countries": total_countries,
        "total_companies": total_companies,
        "assets_by_status": {
            status: count for status, count in status_counts
        },
        "generated_at": datetime.utcnow()
    }
