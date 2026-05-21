from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..core.security import get_current_user
from ..core.config import settings
from ..models.asset import Asset
from ..models.asset_status import AssetStatus
from ..models.user import User
from ..models.staff import Staff
from ..models.stock_location import StockLocation
from ..models.asset_condition_report import AssetConditionReport
from ..schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from ..services.asset_id_generator import AssetIDGenerator
from ..services.qr_code_service import QRCodeService
from ..services.file_upload_service import FileUploadService
from ..models.main_category import MainCategory
import json

router = APIRouter(prefix="/assets", tags=["assets"])

def _normalize_stockid(value):
    if value is None or value == "":
        return None
    if isinstance(value, list):
        return [int(v) for v in value if v is not None and v != ""]
    return [int(value)]

def _first_stockid(stockid_value):
    if not stockid_value:
        return None
    if isinstance(stockid_value, list):
        return stockid_value[0] if stockid_value else None
    return stockid_value

def _format_user_name(user: User) -> Optional[str]:
    if not user:
        return None
    if user.full_name and user.full_name.strip():
        return user.full_name.strip()
    first = (user.firstname or "").strip()
    last = (user.lastname or "").strip()
    full = f"{first} {last}".strip()
    return full or user.email

def _format_staff_name(staff: Staff) -> Optional[str]:
    if not staff:
        return None
    return (staff.fullname or "").strip() or staff.email


def _parse_attachments(raw: str) -> list:
    """Parse po_attachment_path — supports both single path string and JSON array."""
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith('['):
        try:
            return json.loads(raw)
        except Exception:
            pass
    return [raw]


def _serialize_attachments(paths: list) -> str:
    """Serialize list of file paths to JSON string for storage."""
    return json.dumps(paths)


def _resolve_public_url(path: str) -> str:
    """Convert a stored file path (or JSON array) to publicly accessible URL(s).
    Returns a JSON array string if multiple files, or a single URL string."""
    if not path:
        return path

    # Check if it's a JSON array of paths
    paths = _parse_attachments(path)
    if len(paths) > 1 or (len(paths) == 1 and path.strip().startswith('[')):
        resolved = [_resolve_single_url(p) for p in paths]
        return json.dumps(resolved)

    return _resolve_single_url(path)


def _resolve_single_url(path: str) -> str:
    """Resolve a single file path to a public URL."""
    if not path:
        return path

    # Already a full URL
    if path.startswith('http://') or path.startswith('https://'):
        # Get the live public_url from the storage service (updated when config is saved)
        try:
            from ..services.cloud_storage_service import storage_service
            live_public_url = getattr(storage_service, 'public_url', None) or settings.R2_PUBLIC_URL or ''
            live_endpoint = settings.R2_ENDPOINT_URL or ''
            bucket = getattr(storage_service, 'bucket_name', None) or settings.R2_BUCKET_NAME or ''
        except Exception:
            live_public_url = settings.R2_PUBLIC_URL or ''
            live_endpoint = settings.R2_ENDPOINT_URL or ''
            bucket = settings.R2_BUCKET_NAME or ''

        # Swap private endpoint URL → public URL
        if live_endpoint and live_public_url and path.startswith(live_endpoint.rstrip('/')):
            key = path.replace(f"{live_endpoint.rstrip('/')}/{bucket}/", '').replace(f"{live_endpoint.rstrip('/')}/", '')
            return f"{live_public_url.rstrip('/')}/{key}"

        # Already using some public URL — swap base if public_url changed
        if live_public_url:
            # Extract just the key (po_attachments/filename.pdf) from any r2.dev or custom domain URL
            for prefix in [live_endpoint.rstrip('/') + '/' + bucket + '/', live_endpoint.rstrip('/') + '/']:
                if path.startswith(prefix):
                    key = path.replace(prefix, '')
                    return f"{live_public_url.rstrip('/')}/{key}"

        return path

    # Local path — serve via /uploads static route
    clean = path.replace('\\', '/')
    if not clean.startswith('uploads/'):
        clean = f"uploads/{clean.lstrip('/')}"
    return f"http://localhost:8000/{clean}"

@router.get("/", response_model=List[AssetResponse])
def list_assets(
    skip: int = 0,
    limit: int = 100,
    statusid: Optional[int] = None,
    categoryid: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from sqlalchemy.orm import joinedload
    
    query = db.query(Asset).options(
        joinedload(Asset.main_category),
        joinedload(Asset.category),
        joinedload(Asset.country),
        joinedload(Asset.province),
        joinedload(Asset.company),
        joinedload(Asset.location),
        joinedload(Asset.department),
        joinedload(Asset.status)
    )
    
    if statusid:
        query = query.filter(Asset.statusid == statusid)
    if categoryid:
        query = query.filter(Asset.categoryid == categoryid)
    
    assets = query.offset(skip).limit(limit).all()
    assigned_user_ids = {asset.assignedto for asset in assets if asset.assignedto}
    stock_ids = {_first_stockid(asset.stockid) for asset in assets if _first_stockid(asset.stockid)}
    users_by_id = {}
    staff_by_id = {}
    stock_by_id = {}
    if assigned_user_ids:
        staff_members = db.query(Staff).filter(Staff.staffid.in_(assigned_user_ids)).all()
        staff_by_id = {staff.staffid: staff for staff in staff_members}
        users = db.query(User).filter(User.userid.in_(assigned_user_ids)).all()
        users_by_id = {user.userid: user for user in users}
    if stock_ids:
        stocks = db.query(StockLocation).filter(StockLocation.stockid.in_(stock_ids)).all()
        stock_by_id = {stock.stockid: stock for stock in stocks}
    
    # Convert to response format with related data
    response_assets = []
    for asset in assets:
        asset_dict = {
            'assetid': asset.assetid,
            'assetcode': asset.assetcode,
            'assetname': asset.assetname,
            'serialnumber': asset.serialnumber,
            'modelnumber': asset.modelnumber,
            'manufacturer': asset.manufacturer,
            'maincategoryid': asset.maincategoryid,
            'categoryid': asset.categoryid,
            'countryid': asset.countryid,
            'provinceid': asset.provinceid,
            'companyid': asset.companyid,
            'locationid': asset.locationid,
            'departmentid': asset.departmentid,
            'stockid': asset.stockid,
            'assignedto': asset.assignedto,
            'assigneddate': asset.assigneddate,
            'purchasedate': asset.purchasedate,
            'purchaseprice': asset.purchaseprice,
            'currentvalue': asset.currentvalue,
            'depreciationrate': asset.depreciationrate,
            'warrantyexpiry': asset.warrantyexpiry,
            'po_number': asset.po_number,
            'po_attachment_path': _resolve_public_url(asset.po_attachment_path),
            'cost_center': asset.cost_center,
            'statusid': asset.statusid,
            'condition': asset.condition,
            'specifications': asset.specifications,
            'notes': asset.notes,
            'qrcode': asset.qrcode,
            'isactive': asset.isactive,
            'createdat': asset.createdat,
            'updatedat': asset.updatedat,
            'createdby': asset.createdby,
            
            # Add related data for frontend display
            'main_category_name': asset.main_category.categoryname if asset.main_category else None,
            'category_name': asset.category.name if asset.category else None,
            'country_name': asset.country.countryname if asset.country else None,
            'province_name': asset.province.provincename if asset.province else None,
            'company_name': asset.company.companyname if asset.company else None,
            'location_name': asset.location.name if asset.location else None,
            'department_name': asset.department.departmentname if asset.department else None,
            'status_name': asset.status.statusname if asset.status else None,
            'assigned_user_name': (
                _format_staff_name(staff_by_id.get(asset.assignedto))
                or _format_user_name(users_by_id.get(asset.assignedto))
            ) if asset.assignedto else None,
            'stock_location_name': (
                stock_by_id.get(_first_stockid(asset.stockid)).stockname
                if _first_stockid(asset.stockid) in stock_by_id else "Not on stock"
            ),
        }
        response_assets.append(asset_dict)
    
    return response_assets

@router.post("/", response_model=AssetResponse)
def create_asset(asset_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create new asset - handles both old and new data formats
    """
    try:
        # Import required models
        from ..models.asset_status import AssetStatus
        from ..models.location import Location
        
        # 1. Get main category ID from name if provided as string
        if 'main_category' in asset_data and isinstance(asset_data['main_category'], str):
            category = db.query(MainCategory).filter(
                MainCategory.categoryname == asset_data['main_category']
            ).first()
            if not category:
                raise HTTPException(status_code=400, detail=f"Category '{asset_data['main_category']}' not found")
            asset_data['maincategoryid'] = category.maincategoryid
            del asset_data['main_category']
        
        # 2. Get status ID from name if provided as string
        if 'status' in asset_data and isinstance(asset_data['status'], str):
            status = db.query(AssetStatus).filter(
                AssetStatus.statusname == asset_data['status']
            ).first()
            if not status:
                # Default to first status (Available)
                status = db.query(AssetStatus).first()
            asset_data['statusid'] = status.statusid if status else 1
            del asset_data['status']
        elif 'statusid' not in asset_data:
            # Default to first status
            status = db.query(AssetStatus).first()
            asset_data['statusid'] = status.statusid if status else 1
        
        # 3. Handle location - use company's location or create default
        if 'locationid' not in asset_data or asset_data['locationid'] == 0 or asset_data['locationid'] is None:
            company_id = asset_data.get('company_id') or asset_data.get('companyid')
            if company_id:
                location = db.query(Location).filter(
                    Location.companyid == company_id
                ).first()
                if not location:
                    # Create default location for company
                    from ..models.company import Company
                    company = db.query(Company).filter(Company.companyid == company_id).first()
                    location = Location(
                        name=f"{company.companyname} - Main Location" if company else "Default Location",
                        companyid=company_id
                    )
                    db.add(location)
                    db.flush()
                asset_data['locationid'] = location.id
            else:
                # Use first available location as fallback
                location = db.query(Location).first()
                if location:
                    asset_data['locationid'] = location.id
                else:
                    raise HTTPException(status_code=400, detail="No locations available. Please create a location first.")
        
        # 4. Set asset name from brand/model or use default
        if 'assetname' not in asset_data:
            brand = asset_data.get('brand', '')
            model = asset_data.get('model', '')
            asset_data['assetname'] = f"{brand} {model}".strip() or "New Asset"
        
        # 5. Map frontend field names to backend field names
        field_mapping = {
            'country_id': 'countryid',
            'province_id': 'provinceid',
            'company_id': 'companyid',
            'purchase_date': 'purchasedate',
            'purchase_cost': 'purchaseprice',
            'brand': 'manufacturer',
            'model': 'modelnumber',
            'serial_number': 'serialnumber',
            'model_name': 'modelnumber',
            'assigned_to': 'assignedto',
            'assignment_date': 'assigneddate',
        }
        
        for old_name, new_name in field_mapping.items():
            if old_name in asset_data and old_name != new_name:
                asset_data[new_name] = asset_data.pop(old_name)
        
        if 'stockid' in asset_data:
            asset_data['stockid'] = _normalize_stockid(asset_data.get('stockid'))
        
        # 6. Remove fields that aren't in the model
        allowed_fields = {
            'assetname', 'assetcode', 'serialnumber', 'modelnumber', 'manufacturer',
            'maincategoryid', 'categoryid', 'countryid', 'provinceid', 'companyid',
            'locationid', 'departmentid', 'assignedto', 'assigneddate', 'purchasedate',
            'purchaseprice', 'currentvalue', 'depreciationrate', 'warrantyexpiry',
            'statusid', 'condition', 'specifications', 'notes', 'po_number', 'po_attachment_path',
            'cost_center'
        }
        
        # Pack hardware fields into specifications JSON before filtering
        import json as _json
        hw_fields = ['cpu', 'ram', 'hdd', 'wlan_mac', 'lan_mac', 'computer_name', 'accessories']
        hw_data = {k: asset_data.pop(k) for k in hw_fields if k in asset_data and asset_data.get(k)}
        if hw_data:
            existing_specs = asset_data.get('specifications', '')
            try:
                specs = _json.loads(existing_specs) if existing_specs else {}
            except Exception:
                specs = {'raw': existing_specs} if existing_specs else {}
            specs.update(hw_data)
            asset_data['specifications'] = _json.dumps(specs)
        
        asset_data = {k: v for k, v in asset_data.items() if k in allowed_fields}
        
        # 6b. Convert empty strings to None and handle datetime fields properly
        optional_fields = [
            'categoryid', 'departmentid', 'assignedto', 'purchaseprice', 'currentvalue', 
            'depreciationrate', 'condition', 'specifications', 'notes',
            'serialnumber', 'modelnumber', 'manufacturer', 'po_number', 'po_attachment_path',
            'cost_center'
        ]
        
        # Convert empty strings to None for non-datetime fields
        for field in optional_fields:
            if field in asset_data and asset_data[field] == '':
                asset_data[field] = None
        
        # CRITICAL: Handle datetime fields specially to prevent SQLite errors
        datetime_fields = ['assigneddate', 'purchasedate', 'warrantyexpiry']
        for field in datetime_fields:
            if field in asset_data:
                value = asset_data[field]
                
                # Remove if None or empty string
                if value is None or value == '':
                    del asset_data[field]
                    continue
                
                # Convert string to datetime if needed
                if isinstance(value, str):
                    try:
                        asset_data[field] = datetime.fromisoformat(value)
                    except (ValueError, TypeError) as e:
                        print(f"Error converting {field} '{value}' to datetime: {e}")
                        # Remove field if conversion fails
                        del asset_data[field]
                        continue
                
                # If it's already a datetime object, keep it as-is
                elif not isinstance(value, datetime):
                    print(f"Unexpected type for {field}: {type(value)}, removing field")
                    del asset_data[field]
        
        # 7. Get main category name for ID generation
        main_category = db.query(MainCategory).filter(
            MainCategory.maincategoryid == asset_data['maincategoryid']
        ).first()
        
        if not main_category:
            raise HTTPException(status_code=400, detail="Main category not found")
        
        # 8. Generate asset code
        purchase_date_str = None
        if asset_data.get('purchasedate'):
            pd = asset_data['purchasedate']
            # Handle both string and datetime objects
            if isinstance(pd, str):
                purchase_date_str = pd
            elif hasattr(pd, 'isoformat'):
                purchase_date_str = pd.isoformat()
        
        asset_code = AssetIDGenerator.generate_asset_id(
            db=db,
            main_category=main_category.categoryname,
            country_id=asset_data['countryid'],
            province_id=asset_data['provinceid'],
            company_id=asset_data['companyid'],
            purchase_date=purchase_date_str
        )
        
        # 9. Generate QR code
        qr_code = QRCodeService.generate_asset_qr(
            asset_id=asset_code,
            asset_name=asset_data['assetname']
        )
        
        # 10. Add generated fields and ensure datetime fields are set
        asset_data['assetcode'] = asset_code
        asset_data['qrcode'] = qr_code
        asset_data['createdby'] = current_user.userid
        asset_data['isactive'] = 1  # Use 1 for true (integer, not boolean)
        
        # Ensure datetime fields are set to avoid SQLite issues
        now = datetime.utcnow()
        asset_data['createdat'] = now
        asset_data['updatedat'] = now
        
        # 11. Create asset
        db_asset = Asset(**asset_data)
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error creating asset: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/with-file", response_model=AssetResponse)
def create_asset_with_file(
    asset_data: str = Form(...),
    po_attachment: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new asset with optional file upload for PO attachment"""
    try:
        asset_dict = json.loads(asset_data)
        asset_dict.pop('po_attachment', None)

        # Create asset first to get asset code
        created_asset = create_asset(asset_dict, db, current_user)

        # Save file if provided
        if po_attachment and po_attachment.filename:
            file_path = FileUploadService.save_file(po_attachment, created_asset.assetcode)
            existing = _parse_attachments(created_asset.po_attachment_path)
            existing.append(file_path)
            created_asset.po_attachment_path = _serialize_attachments(existing)
            db.commit()
            db.refresh(created_asset)

        return created_asset

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception as e:
        db.rollback()
        print(f"Error creating asset with file: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from sqlalchemy.orm import joinedload
    asset = db.query(Asset).options(
        joinedload(Asset.main_category),
        joinedload(Asset.category),
        joinedload(Asset.country),
        joinedload(Asset.province),
        joinedload(Asset.company),
        joinedload(Asset.location),
        joinedload(Asset.department),
        joinedload(Asset.status)
    ).filter(Asset.assetid == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    assigned_staff = db.query(Staff).filter(Staff.staffid == asset.assignedto).first() if asset.assignedto else None
    assigned_user = db.query(User).filter(User.userid == asset.assignedto).first() if asset.assignedto else None
    stock = db.query(StockLocation).filter(StockLocation.stockid == _first_stockid(asset.stockid)).first() if _first_stockid(asset.stockid) else None
    
    # Build response with related names (same as list endpoint)
    return {
        'assetid': asset.assetid,
        'assetcode': asset.assetcode,
        'assetname': asset.assetname,
        'serialnumber': asset.serialnumber,
        'modelnumber': asset.modelnumber,
        'manufacturer': asset.manufacturer,
        'maincategoryid': asset.maincategoryid,
        'categoryid': asset.categoryid,
        'countryid': asset.countryid,
        'provinceid': asset.provinceid,
        'companyid': asset.companyid,
        'locationid': asset.locationid,
        'departmentid': asset.departmentid,
        'stockid': asset.stockid,
        'assignedto': asset.assignedto,
        'assigneddate': asset.assigneddate,
        'purchasedate': asset.purchasedate,
        'purchaseprice': asset.purchaseprice,
        'currentvalue': asset.currentvalue,
        'depreciationrate': asset.depreciationrate,
        'warrantyexpiry': asset.warrantyexpiry,
        'po_number': asset.po_number,
        'po_attachment_path': _resolve_public_url(asset.po_attachment_path),
        'cost_center': asset.cost_center,
        'statusid': asset.statusid,
        'condition': asset.condition,
        'specifications': asset.specifications,
        'notes': asset.notes,
        'qrcode': asset.qrcode,
        'isactive': asset.isactive,
        'createdat': asset.createdat,
        'updatedat': asset.updatedat,
        'createdby': asset.createdby,
        # Related names
        'main_category_name': asset.main_category.categoryname if asset.main_category else None,
        'category_name': asset.category.name if asset.category else None,
        'country_name': asset.country.countryname if asset.country else None,
        'province_name': asset.province.provincename if asset.province else None,
        'company_name': asset.company.companyname if asset.company else None,
        'location_name': asset.location.name if asset.location else None,
        'department_name': asset.department.departmentname if asset.department else None,
        'status_name': asset.status.statusname if asset.status else None,
        'assigned_user_name': _format_staff_name(assigned_staff) or (_format_user_name(assigned_user) if assigned_user else None),
        'stock_location_name': stock.stockname if stock else "Not on stock",
    }


@router.post("/{asset_id}/checkin")
def checkin_asset(
    asset_id: int,
    stockid: int,
    payload: dict = Body(default={}),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(Asset.assetid == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    stock = db.query(StockLocation).filter(StockLocation.stockid == stockid).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock location not found")

    condition_value = payload.get("condition")
    status_id = None
    if condition_value == "Damaged":
        maintenance_status = db.query(AssetStatus).filter(AssetStatus.statusname.ilike("maintenance")).first()
        status_id = maintenance_status.statusid if maintenance_status else None
    elif condition_value == "Broken":
        retired_status = db.query(AssetStatus).filter(AssetStatus.statusname.ilike("retired")).first()
        status_id = retired_status.statusid if retired_status else None
    else:
        available_status = db.query(AssetStatus).filter(AssetStatus.statusname.ilike("available")).first()
        status_id = available_status.statusid if available_status else None

    previous_assignedto = asset.assignedto
    asset.stockid = [stockid]
    asset.assignedto = None
    asset.assigneddate = None
    if condition_value:
        asset.condition = condition_value
    if status_id:
        asset.statusid = status_id
    asset.updatedat = datetime.utcnow()

    # Record full condition report
    report = AssetConditionReport(
        assetid=asset.assetid,
        action="CHECKIN",
        staffid=previous_assignedto,
        userid=current_user.userid,
        overall_condition=condition_value,
        physical_condition=json.dumps(payload.get("physicalCondition")) if payload.get("physicalCondition") is not None else None,
        functional_test=json.dumps(payload.get("functionalTest")) if payload.get("functionalTest") is not None else None,
        accessories=json.dumps(payload.get("accessories")) if payload.get("accessories") is not None else None,
        notes=payload.get("reason") or payload.get("notes")
    )
    db.add(report)

    db.commit()
    db.refresh(asset)
    return {
        "message": "Asset checked in successfully",
        "assetid": asset.assetid,
        "stockid": asset.stockid,
        "stock_location_name": stock.stockname,
        "statusid": asset.statusid
    }


@router.post("/{asset_id}/checkout")
def checkout_asset(
    asset_id: int,
    assignedto: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(Asset.assetid == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Business rule: only assets in Good condition can be checked out
    if (asset.condition or "").strip().lower() != "good":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot checkout asset. Current condition is '{asset.condition or 'Unknown'}'. Only 'Good' condition is allowed."
        )

    in_use_status = db.query(AssetStatus).filter(AssetStatus.statusname.ilike("in use")).first()
    if not in_use_status:
        in_use_status = db.query(AssetStatus).filter(AssetStatus.statuscode.ilike("IN_USE")).first()

    asset.stockid = [0]
    asset.assignedto = assignedto
    asset.assigneddate = datetime.utcnow() if assignedto else None
    if in_use_status:
        asset.statusid = in_use_status.statusid
    asset.updatedat = datetime.utcnow()

    db.commit()
    db.refresh(asset)
    return {
        "message": "Asset checked out successfully",
        "assetid": asset.assetid,
        "stockid": asset.stockid,
        "stock_location_name": "Not on stock",
        "statusid": asset.statusid
    }


@router.get("/{asset_id}/condition-reports")
def get_asset_condition_reports(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(Asset.assetid == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    reports = db.query(AssetConditionReport).filter(
        AssetConditionReport.assetid == asset_id
    ).order_by(AssetConditionReport.created_at.desc()).all()

    return [
        {
            "reportid": r.reportid,
            "assetid": r.assetid,
            "action": r.action,
            "staffid": r.staffid,
            "userid": r.userid,
            "overall_condition": r.overall_condition,
            "physical_condition": json.loads(r.physical_condition) if r.physical_condition else None,
            "functional_test": json.loads(r.functional_test) if r.functional_test else None,
            "accessories": json.loads(r.accessories) if r.accessories else None,
            "notes": r.notes,
            "created_at": r.created_at,
        }
        for r in reports
    ]

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update existing asset - handles both old and new data formats
    """
    try:
        db_asset = db.query(Asset).filter(Asset.assetid == asset_id).first()
        if not db_asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # Import required models
        from ..models.asset_status import AssetStatus
        
        # 1. Get status ID from name if provided as string
        if 'status' in asset_data and isinstance(asset_data['status'], str):
            status = db.query(AssetStatus).filter(
                AssetStatus.statusname == asset_data['status']
            ).first()
            if status:
                asset_data['statusid'] = status.statusid
            del asset_data['status']
        
        # 2. Map frontend field names to backend field names
        field_mapping = {
            'country_id': 'countryid',
            'province_id': 'provinceid',
            'company_id': 'companyid',
            'purchase_date': 'purchasedate',
            'purchase_cost': 'purchaseprice',
            'brand': 'manufacturer',
            'model': 'modelnumber',
            'serial_number': 'serialnumber',
            'model_name': 'assetname',
            'assigned_to': 'assignedto',
            'assignment_date': 'assigneddate',
            'description': 'notes',
        }
        
        for old_name, new_name in field_mapping.items():
            if old_name in asset_data and old_name != new_name:
                asset_data[new_name] = asset_data.pop(old_name)
        
        if 'stockid' in asset_data:
            asset_data['stockid'] = _normalize_stockid(asset_data.get('stockid'))
        
        # 3. Remove fields that can't be updated (Asset ID generation fields)
        protected_fields = [
            'assetid', 'assetcode', 'qrcode', 'createdat', 'createdby',
            # Asset ID generation fields - cannot be changed
            'maincategoryid', 'countryid', 'provinceid', 'companyid', 'purchasedate'
        ]
        for field in protected_fields:
            asset_data.pop(field, None)
        
        # 4. Convert empty strings to None for optional fields and handle datetime fields
        optional_fields = [
            'categoryid', 'departmentid', 'assignedto', 'assigneddate', 
            'purchasedate', 'purchaseprice', 'currentvalue', 'depreciationrate',
            'warrantyexpiry', 'condition', 'specifications', 'notes',
            'serialnumber', 'modelnumber', 'manufacturer', 'po_number', 'po_attachment_path',
            'cost_center'
        ]
        
        # Handle datetime fields specifically
        datetime_fields = ['assigneddate', 'purchasedate', 'warrantyexpiry']
        
        for field in optional_fields:
            if field in asset_data and asset_data[field] == '':
                asset_data[field] = None
        
        # Remove None datetime fields to avoid SQLite issues
        for field in datetime_fields:
            if field in asset_data and asset_data[field] is None:
                del asset_data[field]
        
        # 5. Update only provided fields - with safety checks
        for key, value in list(asset_data.items()):
            if not hasattr(db_asset, key):
                print(f"Skipping unknown field: {key}")
                continue
            
            # Allow None for assignedto (to unassign asset)
            if value is None and key != 'assignedto':
                print(f"Skipping field {key} - value is None")
                continue
            
            # Skip if value is a list, dict, or other non-scalar type
            if isinstance(value, (list, dict)):
                print(f"Skipping field {key} - invalid type {type(value)}")
                continue
            
            try:
                setattr(db_asset, key, value)
            except Exception as e:
                print(f"Error setting field {key} to {value}: {e}")
                continue
        
        # 6. Update timestamp
        db_asset.updatedat = datetime.utcnow()
        
        db.commit()
        db.refresh(db_asset)
        return db_asset
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating asset: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{asset_id}/with-file", response_model=AssetResponse)
def update_asset_with_file(
    asset_id: int,
    asset_data: str = Form(...),
    po_attachment: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update existing asset with optional file upload for PO attachment
    Handles both new file uploads and file deletion
    """
    try:
        # Parse JSON data from form
        asset_dict = json.loads(asset_data)
        print(f"DEBUG: Received asset_data keys: {list(asset_dict.keys())}")
        print(f"DEBUG: po_attachment_path: {asset_dict.get('po_attachment_path')}")
        
        # Get existing asset
        db_asset = db.query(Asset).filter(Asset.assetid == asset_id).first()
        if not db_asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # Handle file updates
        # If po_attachment_path is provided in asset_dict, use it (user may have deleted files)
        # Otherwise, keep existing files and append new ones
        if 'po_attachment_path' in asset_dict and asset_dict['po_attachment_path']:
            # User sent updated file list (may have deleted some files)
            existing_files = _parse_attachments(asset_dict['po_attachment_path'])
            print(f"DEBUG: Using provided file list: {existing_files}")
        else:
            # No file list provided, keep existing files
            existing_files = _parse_attachments(db_asset.po_attachment_path)
            print(f"DEBUG: Keeping existing files: {existing_files}")
        
        # Handle new file upload if provided
        if po_attachment and po_attachment.filename:
            file_path = FileUploadService.save_file(po_attachment, db_asset.assetcode)
            existing_files.append(file_path)
            print(f"DEBUG: Added new file: {file_path}")
        
        # Update the file list in asset_dict
        asset_dict['po_attachment_path'] = _serialize_attachments(existing_files)
        print(f"DEBUG: Final file list: {asset_dict['po_attachment_path']}")

        # Strip non-model fields that came from the frontend (names, codes, etc.)
        non_model_fields = {
            'assetcode', 'assetid', 'main_category', 'main_category_name', 'category_name',
            'country_name', 'province_name', 'company_name', 'location_name',
            'department_name', 'status_name', 'assigned_user_name',
            'country_id', 'province_id', 'company_id', 'purchase_date',
            'po_attachment', 'po_attachment_path_old',
            'assetcode', 'qrcode', 'createdat', 'createdby',
            'cpu', 'ram', 'hdd', 'wlan_mac', 'lan_mac', 'computer_name', 'accessories',
            'po_attachment_existing',  # Remove frontend-only field
        }
        asset_dict = {k: v for k, v in asset_dict.items() if k not in non_model_fields}
        print(f"DEBUG: After filtering, asset_dict keys: {list(asset_dict.keys())}")

        # Update asset normally
        return update_asset(asset_id, asset_dict, db, current_user)
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating asset with file: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_asset = db.query(Asset).filter(Asset.assetid == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Soft delete
    db_asset.isactive = False
    db.commit()
    return {"message": "Asset deleted successfully"}
