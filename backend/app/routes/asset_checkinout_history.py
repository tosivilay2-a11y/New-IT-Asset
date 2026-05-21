from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.asset_checkinout_history import AssetCheckInOutHistory
from ..models.staff import Staff
from ..models.user import User
from ..models.location import Location
from ..models.company import Company
from ..schemas.asset_checkinout_history import AssetCheckInOutHistoryResponse, AssetCheckInOutHistoryCreate

router = APIRouter(prefix="/asset-history", tags=["asset-history"])

@router.get("/asset/{asset_id}", response_model=List[AssetCheckInOutHistoryResponse])
def get_asset_history(asset_id: int, db: Session = Depends(get_db)):
    """Get check-in/check-out history for an asset"""
    history = db.query(AssetCheckInOutHistory).filter(
        AssetCheckInOutHistory.assetid == asset_id
    ).order_by(AssetCheckInOutHistory.created_at.desc()).all()
    
    # Enrich response with readable names for UI
    staff_ids = {h.staffid for h in history if h.staffid}
    user_ids = {h.userid for h in history if h.userid}
    location_ids = {h.location_before for h in history if h.location_before} | {h.location_after for h in history if h.location_after}

    staff_map = {}
    user_map = {}
    location_map = {}
    company_map = {}

    if staff_ids:
        staff_rows = db.query(Staff).filter(Staff.staffid.in_(staff_ids)).all()
        staff_map = {s.staffid: s for s in staff_rows}
    if user_ids:
        user_rows = db.query(User).filter(User.userid.in_(user_ids)).all()
        user_map = {u.userid: u for u in user_rows}
    if location_ids:
        location_rows = db.query(Location).filter(Location.id.in_(location_ids)).all()
        company_rows = db.query(Company).filter(Company.companyid.in_(location_ids)).all()
        location_map = {l.id: l.name for l in location_rows}
        company_map = {c.companyid: c.companyname for c in company_rows}

    enriched = []
    for h in history:
        staff_name = staff_map.get(h.staffid).fullname if h.staffid and h.staffid in staff_map else None
        user_obj = user_map.get(h.userid) if h.userid else None
        user_name = None
        if user_obj:
            user_name = f"{(user_obj.firstname or '').strip()} {(user_obj.lastname or '').strip()}".strip() or user_obj.full_name or user_obj.email

        before_name = location_map.get(h.location_before) or company_map.get(h.location_before)
        after_name = location_map.get(h.location_after) or company_map.get(h.location_after)

        enriched.append({
            "historyid": h.historyid,
            "assetid": h.assetid,
            "action": h.action,
            "userid": h.userid,
            "staffid": h.staffid,
            "reason": h.reason,
            "condition_before": h.condition_before,
            "condition_after": h.condition_after,
            "location_before": h.location_before,
            "location_after": h.location_after,
            "notes": h.notes,
            "created_at": h.created_at,
            "staff_name": staff_name,
            "user_name": user_name,
            "location_before_name": before_name,
            "location_after_name": after_name,
        })

    return enriched

@router.post("/", response_model=AssetCheckInOutHistoryResponse)
def create_history(
    history_data: AssetCheckInOutHistoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new history record"""
    db_history = AssetCheckInOutHistory(
        assetid=history_data.assetid,
        action=history_data.action,
        userid=history_data.userid,
        staffid=history_data.staffid,
        reason=history_data.reason,
        condition_before=history_data.condition_before,
        condition_after=history_data.condition_after,
        location_before=history_data.location_before,
        location_after=history_data.location_after,
        notes=history_data.notes
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
