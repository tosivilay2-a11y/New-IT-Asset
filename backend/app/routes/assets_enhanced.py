"""
Enhanced Asset Management Routes
Complete CRUD operations with QR codes, ID generation, and lifecycle management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.asset import Asset
from ..models.user import User
from ..services.asset_id_generator import AssetIDGenerator
from ..services.qr_code_service import QRCodeService
from pydantic import BaseModel

router = APIRouter(prefix="/api/assets", tags=["assets"])

# Pydantic Schemas
class AssetCreate(BaseModel):
    name: str
    category_code: str
    country_id: int
    province_code: str
    company_id: int
    country_code: str
    company_code: str
    # Basic info
    brand: Optional[str] = None
    model: Optional[str] = None
    # Technical specs
    cpu: Optional[str] = None
    ram: Optional[str] = None
    hdd: Optional[str] = None
    # Purchase info
    purchase_date: Optional[date] = None
    value: Optional[float] = None
    # Location
    location_id: Optional[int] = None
    # Assignment
    assigned_user_id: Optional[int] = None

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    cpu: Optional[str] = None
    ram: Optional[str] = None
    hdd: Optional[str] = None
    purchase_date: Optional[date] = None
    value: Optional[float] = None
    location_id: Optional[int] = None
    assigned_user_id: Optional[int] = None

class AssetIDPreview(BaseModel):
    category_code: str
    country_code: str
    province_code: str
    company_code: str

# =============================================
# ASSET ID GENERATION
# =============================================

@router.post("/preview-id")
async def preview_asset_id(
    data: AssetIDPreview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Preview what the asset ID will look like"""
    
    # Get next sequence
    from ..models.enhanced_asset import Country, Company
    
    country = db.query(Country).filter(Country.countrycode == data.country_code).first()
    company = db.query(Company).filter(Company.companycode == data.company_code).first()
    
    if not country or not company:
        raise HTTPException(status_code=404, detail="Country or Company not found")
    
    next_seq = AssetIDGenerator.get_next_sequence(db, country.countryid, company.companyid)
    
    preview = AssetIDGenerator.preview_asset_id(
        data.category_code,
        data.country_code,
        data.province_code,
        data.company_code,
        next_seq
    )
    
    return {
        "preview": preview,
        "next_sequence": next_seq,
        "year": datetime.now().year
    }

# =============================================
# ASSET CRUD OPERATIONS
# =============================================

@router.post("/", status_code=201)
async def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new asset with auto-generated ID and QR code"""
    
    # Generate Asset ID
    asset_id = AssetIDGenerator.generate_asset_id(
        db=db,
        category_code=asset_data.category_code,
        country_id=asset_data.country_id,
        province_code=asset_data.province_code,
        company_id=asset_data.company_id,
        country_code=asset_data.country_code,
        company_code=asset_data.company_code
    )
    
    # Generate QR Code
    qr_code = QRCodeService.generate_asset_qr(asset_id, asset_data.name)
    
    # Create asset
    new_asset = Asset(
        asset_id=asset_id,
        name=asset_data.name,
        brand=asset_data.brand,
        model=asset_data.model,
        cpu=asset_data.cpu,
        ram=asset_data.ram,
        hdd=asset_data.hdd,
        purchase_date=asset_data.purchase_date,
        value=asset_data.value,
        location_id=asset_data.location_id,
        assigned_user_id=asset_data.assigned_user_id,
        status="available",
        qrcode=qr_code,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    
    return {
        "success": True,
        "message": "Asset created successfully",
        "asset_id": asset_id,
        "qr_code": qr_code,
        "data": {
            "id": new_asset.id,
            "asset_id": new_asset.asset_id,
            "name": new_asset.name,
            "status": new_asset.status
        }
    }

@router.get("/")
async def list_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    location_id: Optional[int] = None,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all assets with pagination and filters"""
    
    query = db.query(Asset)
    
    # Apply filters
    if status:
        query = query.filter(Asset.status == status)
    if location_id:
        query = query.filter(Asset.location_id == location_id)
    if category_id:
        query = query.filter(Asset.category_id == category_id)
    if search:
        query = query.filter(
            (Asset.asset_id.ilike(f"%{search}%")) |
            (Asset.name.ilike(f"%{search}%")) |
            (Asset.brand.ilike(f"%{search}%"))
        )
    
    total = query.count()
    assets = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [
            {
                "id": asset.id,
                "asset_id": asset.asset_id,
                "name": asset.name,
                "status": asset.status,
                "brand": asset.brand,
                "model": asset.model,
                "location_id": asset.location_id,
                "assigned_user_id": asset.assigned_user_id,
                "created_at": asset.created_at
            }
            for asset in assets
        ]
    }

@router.get("/{asset_id}")
async def get_asset(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get asset details by asset ID"""
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return {
        "id": asset.id,
        "asset_id": asset.asset_id,
        "name": asset.name,
        "status": asset.status,
        "brand": asset.brand,
        "model": asset.model,
        "cpu": asset.cpu,
        "ram": asset.ram,
        "hdd": asset.hdd,
        "purchase_date": asset.purchase_date,
        "value": asset.value,
        "location_id": asset.location_id,
        "assigned_user_id": asset.assigned_user_id,
        "qr_code": asset.qrcode if hasattr(asset, 'qrcode') else None,
        "created_at": asset.created_at,
        "updated_at": asset.updated_at
    }

@router.put("/{asset_id}")
async def update_asset(
    asset_id: str,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update asset information"""
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Update fields
    update_data = asset_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)
    
    asset.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(asset)
    
    return {
        "success": True,
        "message": "Asset updated successfully",
        "data": {
            "asset_id": asset.asset_id,
            "name": asset.name,
            "status": asset.status
        }
    }

@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete/deactivate asset (Admin only)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Soft delete - change status to disposed
    asset.status = "disposed"
    asset.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Asset deactivated successfully"
    }

# =============================================
# QR CODE OPERATIONS
# =============================================

@router.get("/{asset_id}/qr-code")
async def get_asset_qr_code(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get QR code for specific asset"""
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Generate if not exists
    if not hasattr(asset, 'qrcode') or not asset.qrcode:
        qr_code = QRCodeService.generate_asset_qr(asset.asset_id, asset.name)
        asset.qrcode = qr_code
        db.commit()
    else:
        qr_code = asset.qrcode
    
    return {
        "asset_id": asset.asset_id,
        "qr_code": qr_code
    }

@router.post("/bulk-qr-codes")
async def generate_bulk_qr_codes(
    asset_ids: List[str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate QR codes for multiple assets"""
    
    qr_codes = QRCodeService.generate_bulk_qr_codes(asset_ids)
    
    return {
        "success": True,
        "count": len(qr_codes),
        "qr_codes": qr_codes
    }

# =============================================
# ASSET LIFECYCLE
# =============================================

@router.post("/{asset_id}/assign")
async def assign_asset(
    asset_id: str,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign asset to user"""
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    if asset.status != "available":
        raise HTTPException(status_code=400, detail="Asset is not available")
    
    asset.assigned_user_id = user_id
    asset.status = "in_use"
    asset.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Asset assigned successfully"
    }

@router.post("/{asset_id}/return")
async def return_asset(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return asset (check-in)"""
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    asset.assigned_user_id = None
    asset.status = "available"
    asset.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Asset returned successfully"
    }

@router.post("/{asset_id}/transfer")
async def transfer_asset(
    asset_id: str,
    new_location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Transfer asset to new location"""
    
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    old_location = asset.location_id
    asset.location_id = new_location_id
    asset.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Asset transferred successfully",
        "old_location": old_location,
        "new_location": new_location_id
    }
