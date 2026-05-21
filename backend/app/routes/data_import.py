"""
Data Import / Export — batch assets and staff (Excel & CSV)
Columns aligned with PostgreSQL `assets` table and related lookup tables.
"""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import require_admin
from ..models.user import User
from ..models.asset import Asset
from ..models.staff import Staff
from ..models.company import Company
from ..models.location import Location
from ..services.excel_utils import (
    build_xlsx,
    get_cell,
    normalize_row,
    parse_upload_file,
)
from ..services.asset_import_schema import ASSET_DB_COLUMNS
from ..services.asset_import_service import (
    asset_to_export_row,
    build_template_bytes,
    import_asset_row,
)

router = APIRouter(prefix="/data-import", tags=["data-import"])


class BatchImportResult(BaseModel):
    imported_count: int
    error_count: int
    errors: List[str]


STAFF_TEMPLATE_HEADERS = [
    "Employee ID",
    "Full Name",
    "Email",
    "Department",
    "Position",
    "Company",
    "Location",
    "Employment Status",
]

STAFF_EXPORT_HEADERS = [
    "Employee ID",
    "Full Name",
    "Email",
    "Department",
    "Position",
    "Company",
    "Location",
    "Employment Status",
]


def _excel_response(content: bytes, filename: str) -> Response:
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def _lookup_company(db: Session, value: str):
    return db.query(Company).filter(
        (Company.companyname.ilike(value)) | (Company.companycode.ilike(value))
    ).first()


def _lookup_location(db: Session, value: str, company_id=None):
    q = db.query(Location).filter(Location.name.ilike(value))
    if company_id:
        q = q.filter(Location.companyid == company_id)
    return q.first()


# ─── Asset templates & export ─────────────────────────────────────────────────

@router.get("/assets/template")
def download_asset_template(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Import sheet uses exact public.assets columns; ref_* sheets + ID dropdowns."""
    content = build_template_bytes(db)
    return _excel_response(content, "asset_import_template.xlsx")


@router.get("/assets/export")
def export_assets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    assets = db.query(Asset).order_by(Asset.assetid).all()
    rows = [asset_to_export_row(a) for a in assets]
    content = build_xlsx(ASSET_DB_COLUMNS, rows, "Import")
    return _excel_response(
        content,
        f"assets_export_{datetime.utcnow().strftime('%Y%m%d')}.xlsx",
    )


@router.post("/assets/import", response_model=BatchImportResult)
async def import_assets_batch(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    content = await file.read()
    try:
        raw_rows = parse_upload_file(content, file.filename or "")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    imported = 0
    errors: List[str] = []

    for idx, raw in enumerate(raw_rows, start=2):
        asset, err = import_asset_row(db, raw, idx, current_user)
        if err:
            errors.append(err)
            continue
        db.add(asset)
        db.flush()
        imported += 1

    if imported:
        db.commit()
    else:
        db.rollback()

    return BatchImportResult(
        imported_count=imported,
        error_count=len(errors),
        errors=errors[:50],
    )


# ─── Staff templates & export ─────────────────────────────────────────────────

@router.get("/staff/template")
def download_staff_template(current_user: User = Depends(require_admin)):
    sample = [
        "EMP001",
        "John Doe",
        "john@example.com",
        "IT",
        "Developer",
        "AVIS",
        "Head Office",
        "Active",
    ]
    content = build_xlsx(STAFF_TEMPLATE_HEADERS, [sample], "Staff")
    return _excel_response(content, "staff_import_template.xlsx")


@router.get("/staff/export")
def export_staff(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    staff_list = db.query(Staff).order_by(Staff.staffid).all()
    company_ids = {s.companyid for s in staff_list if s.companyid}
    location_ids = {s.locationid for s in staff_list if s.locationid}

    companies = {
        c.companyid: c.companyname
        for c in db.query(Company).filter(Company.companyid.in_(company_ids)).all()
    } if company_ids else {}
    locations = {
        loc.id: loc.name
        for loc in db.query(Location).filter(Location.id.in_(location_ids)).all()
    } if location_ids else {}

    rows = []
    for s in staff_list:
        rows.append([
            s.employeeid,
            s.fullname,
            s.email or "",
            s.department or "",
            s.position or "",
            companies.get(s.companyid, ""),
            locations.get(s.locationid, ""),
            s.employmentstatus or "Active",
        ])

    content = build_xlsx(STAFF_EXPORT_HEADERS, rows, "Staff")
    return _excel_response(
        content,
        f"staff_export_{datetime.utcnow().strftime('%Y%m%d')}.xlsx",
    )


@router.post("/staff/import", response_model=BatchImportResult)
async def import_staff_batch(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    content = await file.read()
    try:
        raw_rows = parse_upload_file(content, file.filename or "")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    imported = 0
    errors: List[str] = []

    for idx, raw in enumerate(raw_rows, start=2):
        row = normalize_row(raw)
        try:
            employeeid = get_cell(row, "employeeid", "employee id")
            fullname = get_cell(row, "fullname", "full name")

            if not employeeid or not fullname:
                errors.append(f"Row {idx}: Employee ID and Full Name are required")
                continue

            employeeid = str(employeeid).strip()
            if db.query(Staff).filter(Staff.employeeid == employeeid).first():
                errors.append(f"Row {idx}: Employee ID '{employeeid}' already exists")
                continue

            email = get_cell(row, "email")
            if email and db.query(Staff).filter(Staff.email == str(email)).first():
                errors.append(f"Row {idx}: Email '{email}' already exists")
                continue

            companyid = None
            company_val = get_cell(row, "company", "companyname")
            if company_val:
                company = _lookup_company(db, str(company_val))
                if not company:
                    errors.append(f"Row {idx}: Company '{company_val}' not found")
                    continue
                companyid = company.companyid

            locationid = None
            location_val = get_cell(row, "location", "locationname")
            if location_val:
                location = _lookup_location(
                    db, str(location_val), companyid
                )
                if not location:
                    errors.append(f"Row {idx}: Location '{location_val}' not found")
                    continue
                locationid = location.id

            db_staff = Staff(
                employeeid=employeeid,
                fullname=str(fullname).strip(),
                email=str(email).strip() if email else None,
                department=get_cell(row, "department"),
                position=get_cell(row, "position"),
                employmentstatus=str(
                    get_cell(row, "employmentstatus", "employment status") or "Active"
                ),
                companyid=companyid,
                locationid=locationid,
            )
            db.add(db_staff)
            db.flush()
            imported += 1

        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")

    if imported:
        db.commit()
    else:
        db.rollback()

    return BatchImportResult(
        imported_count=imported,
        error_count=len(errors),
        errors=errors[:50],
    )
