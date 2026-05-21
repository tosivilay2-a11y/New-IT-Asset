from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.staff import Staff
from ..models.asset import Asset
from ..models.asset_status import AssetStatus
from ..models.asset_request import AssetRequest
from ..schemas.asset_request import AssetRequestCreate, AssetRequestUpdate, AssetRequestResponse

router = APIRouter(prefix="/asset-requests", tags=["asset-requests"])

@router.get("/", response_model=List[AssetRequestResponse])
def list_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all asset requests"""
    # If the user is admin, they see all. Otherwise, they see their own.
    if current_user.role == "admin":
        return db.query(AssetRequest).order_by(AssetRequest.created_at.desc()).all()
    else:
        return db.query(AssetRequest).filter(AssetRequest.requested_by == current_user.email).order_by(AssetRequest.created_at.desc()).all()

@router.post("/", response_model=AssetRequestResponse)
def create_request(
    request_data: AssetRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new asset request (submitted by HR)"""
    company_name = request_data.company_name
    if request_data.company_id and not company_name:
        from ..models.company import Company
        company = db.query(Company).filter(Company.companyid == request_data.company_id).first()
        if company:
            company_name = company.companyname

    db_request = AssetRequest(
        staff_id=request_data.staff_id,
        staff_name=request_data.staff_name,
        staff_email=request_data.staff_email,
        department=request_data.department,
        position=request_data.position,
        company_id=request_data.company_id,
        company_name=company_name,
        province_id=request_data.province_id,
        location_id=request_data.location_id,
        asset_type=request_data.asset_type,
        priority=request_data.priority,
        reason=request_data.reason,
        notes=request_data.notes,
        status="Pending",
        requested_by=current_user.email
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.put("/{request_id}", response_model=AssetRequestResponse)
def update_request(
    request_id: int,
    request_update: AssetRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update asset request details or status"""
    db_request = db.query(AssetRequest).filter(AssetRequest.requestid == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
        
    if request_update.status is not None:
        db_request.status = request_update.status
    if request_update.notes is not None:
        db_request.notes = request_update.notes
    if request_update.assigned_assetcode is not None:
        db_request.assigned_assetcode = request_update.assigned_assetcode
        
    db_request.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/{request_id}/assign")
def assign_request_asset(
    request_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    IT reviews and signs/assigns a computer to staff.
    """
    # 1. Fetch the request
    db_request = db.query(AssetRequest).filter(AssetRequest.requestid == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
        
    assetcode = payload.get("assetcode")
    if not assetcode:
        raise HTTPException(status_code=400, detail="Asset code is required for assignment")
        
    # 2. Find the asset and check availability
    asset = db.query(Asset).filter(Asset.assetcode == assetcode).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if (asset.condition or "").strip().lower() != "good":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot checkout asset. Current condition is '{asset.condition or 'Unknown'}'. Only 'Good' condition is allowed."
        )
        
    # 3. Create or find Staff member
    db_staff = None
    if db_request.staff_id:
        db_staff = db.query(Staff).filter(Staff.staffid == db_request.staff_id).first()
    if not db_staff and db_request.staff_email:
        db_staff = db.query(Staff).filter(Staff.email == db_request.staff_email).first()
    if not db_staff:
        db_staff = db.query(Staff).filter(Staff.fullname == db_request.staff_name).first()
        
    if not db_staff:
        # Generate a unique employee ID
        emp_id = f"EMP{random.randint(10000, 99999)}"
        while db.query(Staff).filter(Staff.employeeid == emp_id).first():
            emp_id = f"EMP{random.randint(10000, 99999)}"
            
        # Try finding companyid from company name
        companyid = db_request.company_id
        if not companyid and db_request.company_name:
            from ..models.company import Company
            company = db.query(Company).filter(Company.companyname.ilike(db_request.company_name)).first()
            if company:
                companyid = company.companyid
                
        # Resolve geographic details, departmentid, and costcenterid for the new staff profile
        countryid = None
        provinceid = db_request.province_id
        departmentid = None
        costcenterid = None

        if companyid:
            from ..models.company import Company
            company_obj = db.query(Company).filter(Company.companyid == companyid).first()
            if company_obj:
                if not provinceid:
                    provinceid = company_obj.provinceid
                from ..models.province import Province
                province_obj = db.query(Province).filter(Province.provinceid == provinceid).first()
                if province_obj:
                    countryid = province_obj.countryid

        if db_request.department:
            from ..models.department import Department
            # Try to find a formal department belonging to the selected company
            dept_obj = db.query(Department).filter(
                (Department.departmentname.ilike(db_request.department)) & 
                (Department.companyid == companyid)
            ).first()
            # Fallback to any department matching the name
            if not dept_obj:
                dept_obj = db.query(Department).filter(Department.departmentname.ilike(db_request.department)).first()
            
            if dept_obj:
                departmentid = dept_obj.departmentid
                costcenterid = dept_obj.costcenterid

        db_staff = Staff(
            employeeid=emp_id,
            fullname=db_request.staff_name,
            email=db_request.staff_email,
            department=db_request.department,
            position=db_request.position,
            companyid=companyid,
            locationid=db_request.location_id,
            employmentstatus="Active",
            countryid=countryid,
            provinceid=provinceid,
            departmentid=departmentid,
            costcenterid=costcenterid
        )
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)

    # 4. Checkout asset to the staff member
    in_use_status = db.query(AssetStatus).filter(AssetStatus.statusname.ilike("in use")).first()
    if not in_use_status:
        in_use_status = db.query(AssetStatus).filter(AssetStatus.statuscode.ilike("IN_USE")).first()
        
    asset.stockid = [0]
    asset.assignedto = db_staff.staffid
    asset.assigneddate = datetime.utcnow()
    
    # Update asset's location to match staff location if specified, or request location, or keep current
    target_location = db_staff.locationid or db_request.location_id or asset.locationid
    if target_location:
        asset.locationid = target_location
        
    if in_use_status:
        asset.statusid = in_use_status.statusid
    asset.updatedat = datetime.utcnow()
    
    # 5. Record checkout history
    from ..models.asset_checkinout_history import AssetCheckInOutHistory
    history = AssetCheckInOutHistory(
        assetid=asset.assetid,
        action="CHECKOUT",
        staffid=db_staff.staffid,
        reason=db_request.reason or f"Assigned via HR Request Ticket #{request_id}",
        condition_before=asset.condition or "Good",
        condition_after="Good",
        location_before=asset.locationid,
        location_after=target_location,
        notes=f"Checked out to staff member {db_staff.fullname} via HR Request"
    )
    db.add(history)
    
    # 6. Update Request status to Assigned
    db_request.status = "Assigned"
    db_request.assigned_assetcode = assetcode
    db_request.assigned_at = datetime.utcnow()
    if payload.get("notes"):
        db_request.notes = payload.get("notes")
    
    db.commit()
    db.refresh(db_request)
    db.refresh(asset)
    
    return {
        "message": f"Asset {assetcode} successfully assigned and checked out to {db_staff.fullname}",
        "request": {
            "requestid": db_request.requestid,
            "status": db_request.status,
            "assigned_assetcode": db_request.assigned_assetcode
        }
    }
