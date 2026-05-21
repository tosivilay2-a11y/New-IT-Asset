"""
Asset Utilities API Routes
Asset ID generation, QR code generation, etc.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from ..core.database import get_db
from ..services.asset_id_generator import AssetIDGenerator
from ..services.qr_code_service import QRCodeService

router = APIRouter(prefix="/asset-utils", tags=["asset-utils"])

class AssetIDPreviewRequest(BaseModel):
    main_category: str
    country_id: int
    province_id: int
    company_id: int
    purchase_date: Optional[str] = None

class AssetIDGenerateRequest(BaseModel):
    main_category: str
    country_id: int
    province_id: int
    company_id: int
    purchase_date: Optional[str] = None

class QRCodeRequest(BaseModel):
    asset_id: str
    asset_name: Optional[str] = None

@router.post("/preview-asset-id")
def preview_asset_id(request: AssetIDPreviewRequest, db: Session = Depends(get_db)):
    """
    Preview asset ID without incrementing sequence
    Use this in forms to show what the ID will look like
    """
    try:
        asset_id = AssetIDGenerator.preview_asset_id(
            db=db,
            main_category=request.main_category,
            country_id=request.country_id,
            province_id=request.province_id,
            company_id=request.company_id,
            purchase_date=request.purchase_date
        )
        
        # Parse the ID to show components
        parsed = AssetIDGenerator.parse_asset_id(asset_id)
        
        return {
            "asset_id": asset_id,
            "components": parsed,
            "format": "CategoryCode(1) + CountryCode(2) + ProvinceCode(3) + CompanyCode(4) + Year(2) + Sequence(3)",
            "example": "MLALPBAVIS25015"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-asset-id")
def generate_asset_id(request: AssetIDGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate asset ID and increment sequence
    ONLY call when actually saving the asset!
    """
    try:
        asset_id = AssetIDGenerator.generate_asset_id(
            db=db,
            main_category=request.main_category,
            country_id=request.country_id,
            province_id=request.province_id,
            company_id=request.company_id,
            purchase_date=request.purchase_date
        )
        
        return {
            "asset_id": asset_id,
            "message": "Asset ID generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-qr-code")
def generate_qr_code(request: QRCodeRequest):
    """
    Generate QR code for asset
    Returns base64 encoded PNG image
    """
    try:
        qr_code = QRCodeService.generate_asset_qr(
            asset_id=request.asset_id,
            asset_name=request.asset_name
        )
        
        return {
            "qr_code": qr_code,
            "asset_id": request.asset_id,
            "format": "base64 PNG image"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/next-sequence/{country_id}/{company_id}")
def get_next_sequence(country_id: int, company_id: int, db: Session = Depends(get_db)):
    """
    Get next sequence number without incrementing
    """
    try:
        next_seq = AssetIDGenerator.get_next_sequence(db, country_id, company_id)
        return {
            "country_id": country_id,
            "company_id": company_id,
            "next_sequence": next_seq
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/validate-asset-id/{asset_id}")
def validate_asset_id(asset_id: str):
    """
    Validate asset ID format
    """
    is_valid = AssetIDGenerator.validate_asset_id(asset_id)
    
    if is_valid:
        parsed = AssetIDGenerator.parse_asset_id(asset_id)
        return {
            "valid": True,
            "asset_id": asset_id,
            "components": parsed
        }
    else:
        return {
            "valid": False,
            "asset_id": asset_id,
            "message": "Invalid asset ID format. Expected: CategoryCode(1) + CountryCode(2) + ProvinceCode(3) + CompanyCode(4) + Year(2) + Sequence(3)"
        }
