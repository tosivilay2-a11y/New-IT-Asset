"""
Build reference data and import/export rows for public.assets (exact column layout).
"""
import json
from datetime import datetime
from typing import Any, List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload

from ..models.asset import Asset
from ..models.asset_status import AssetStatus
from ..models.category import Category
from ..models.company import Company
from ..models.country import Country
from ..models.department import Department
from ..models.location import Location
from ..models.main_category import MainCategory
from ..models.province import Province
from ..models.staff import Staff
from ..models.stock_location import StockLocation
from ..models.user import User
from .asset_import_resolve import parse_id_value, parse_stockid
from .asset_import_schema import ASSET_DB_COLUMNS, ASSET_REQUIRED_COLUMNS
from .asset_import_workbook import build_asset_import_workbook
from .excel_utils import get_cell, normalize_row
from .qr_code_service import QRCodeService


def _pick(id_val: Any, *labels: str) -> str:
    parts = [str(x) for x in labels if x is not None and str(x).strip()]
    name = " | ".join(parts) if parts else ""
    if id_val is None or str(id_val).strip() == "":
        return ""
    return f"{id_val} - {name}" if name else str(id_val)


def build_asset_reference_sheets(db: Session) -> List[Tuple[str, List[str], List[List[Any]]]]:
    sheets = []

    cats = db.query(MainCategory).filter(MainCategory.isactive == True).all()
    sheets.append((
        "ref_maincategories",
        ["maincategoryid", "categoryname", "categorycode", "pick_list"],
        [[c.maincategoryid, c.categoryname, c.categorycode, _pick(c.maincategoryid, c.categoryname)] for c in cats],
    ))

    subcats = db.query(Category).all()
    sheets.append((
        "ref_categories",
        ["categoryid", "name", "pick_list"],
        [[c.id, c.name, _pick(c.id, c.name)] for c in subcats],
    ))

    countries = db.query(Country).filter(Country.isactive == True).all()
    sheets.append((
        "ref_countries",
        ["countryid", "countryname", "countrycode", "pick_list"],
        [[c.countryid, c.countryname, c.countrycode, _pick(c.countryid, c.countryname)] for c in countries],
    ))

    provinces = (
        db.query(Province).options(joinedload(Province.country)).filter(Province.isactive == True).all()
    )
    sheets.append((
        "ref_provinces",
        ["provinceid", "provincename", "provincecode", "countryid", "pick_list"],
        [
            [p.provinceid, p.provincename, p.provincecode, p.countryid,
             _pick(p.provinceid, p.provincename, p.country.countryname if p.country else "")]
            for p in provinces
        ],
    ))

    companies = db.query(Company).filter(Company.isactive == True).all()
    sheets.append((
        "ref_companies",
        ["companyid", "companyname", "companycode", "provinceid", "pick_list"],
        [[c.companyid, c.companyname, c.companycode, c.provinceid, _pick(c.companyid, c.companyname)] for c in companies],
    ))

    locations = db.query(Location).all()
    sheets.append((
        "ref_locations",
        ["locationid", "name", "companyid", "pick_list"],
        [[loc.id, loc.name, loc.companyid, _pick(loc.id, loc.name)] for loc in locations],
    ))

    depts = db.query(Department).filter(Department.isactive == True).all()
    sheets.append((
        "ref_departments",
        ["departmentid", "departmentname", "departmentcode", "companyid", "pick_list"],
        [[d.departmentid, d.departmentname, d.departmentcode, d.companyid, _pick(d.departmentid, d.departmentname)] for d in depts],
    ))

    statuses = db.query(AssetStatus).filter(AssetStatus.isactive == True).all()
    sheets.append((
        "ref_assetstatuses",
        ["statusid", "statusname", "statuscode", "pick_list"],
        [[s.statusid, s.statusname, s.statuscode, _pick(s.statusid, s.statusname)] for s in statuses],
    ))

    staff_list = db.query(Staff).all()
    sheets.append((
        "ref_staff",
        ["staffid", "employeeid", "fullname", "pick_list"],
        [[s.staffid, s.employeeid, s.fullname, _pick(s.staffid, s.employeeid, s.fullname)] for s in staff_list],
    ))

    stocks = db.query(StockLocation).all()
    sheets.append((
        "ref_stocklocation",
        ["stockid", "stockname", "locationid", "pick_list"],
        [[s.stockid, s.stockname, s.locationid, _pick(s.stockid, s.stockname)] for s in stocks],
    ))

    users = db.query(User).all()
    sheets.append((
        "ref_users",
        ["userid", "email", "pick_list"],
        [[u.userid, u.email, _pick(u.userid, u.email)] for u in users],
    ))

    return sheets


def asset_to_export_row(a: Asset) -> List[Any]:
    def fmt_dt(d):
        if not d:
            return ""
        if isinstance(d, datetime):
            return d.strftime("%Y-%m-%d %H:%M:%S")
        return str(d)

    stock_val = ""
    if a.stockid:
        if isinstance(a.stockid, list):
            stock_val = ",".join(str(x) for x in a.stockid)
        else:
            stock_val = str(a.stockid)

    return [
        a.assetcode,
        a.assetname,
        a.serialnumber or "",
        a.modelnumber or "",
        a.manufacturer or "",
        a.maincategoryid,
        a.categoryid if a.categoryid is not None else "",
        a.countryid,
        a.provinceid,
        a.companyid,
        a.locationid,
        a.departmentid if a.departmentid is not None else "",
        a.assignedto if a.assignedto is not None else "",
        fmt_dt(a.assigneddate),
        fmt_dt(a.purchasedate),
        a.purchaseprice if a.purchaseprice is not None else "",
        a.currentvalue if a.currentvalue is not None else "",
        a.depreciationrate if a.depreciationrate is not None else "",
        fmt_dt(a.warrantyexpiry),
        a.po_number or "",
        a.po_attachment_path or "",
        a.cost_center or "",
        a.statusid,
        a.condition or "",
        a.specifications or "",
        "",  # qrcode omitted from export (too large)
        a.isactive if a.isactive is not None else 1,
        fmt_dt(a.createdat),
        fmt_dt(a.updatedat),
        a.createdby if a.createdby is not None else "",
        a.notes or "",
        stock_val,
    ]


def build_template_bytes(db: Session) -> bytes:
    sample_asset = db.query(Asset).order_by(Asset.assetid.desc()).first()
    if sample_asset:
        sample = asset_to_export_row(sample_asset)
        if len(sample) > 25:
            sample[25] = ""  # clear qrcode in sample
    else:
        sample = [""] * len(ASSET_DB_COLUMNS)
        sample[0] = "YOUR-ASSET-CODE"
        sample[1] = "Asset name"
        sample[5] = 1
        sample[7] = 1
        sample[8] = 1
        sample[9] = 1
        sample[10] = 1
        sample[22] = 1
        sample[26] = 1

    ref_sheets = build_asset_reference_sheets(db)
    return build_asset_import_workbook(sample, ref_sheets)


def _parse_date(value) -> Optional[datetime]:
    if value is None or str(value).strip() == "":
        return None
    if isinstance(value, datetime):
        return value
    s = str(value).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s[:19], fmt)
        except ValueError:
            continue
    return None


def _parse_float(value) -> Optional[float]:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_int_flag(value, default: int = 1) -> int:
    if value is None or str(value).strip() == "":
        return default
    pid = parse_id_value(value)
    if pid is not None:
        return pid
    return default


def import_asset_row(db: Session, raw: dict, row_num: int, current_user: User) -> Tuple[Optional[Asset], Optional[str]]:
    row = normalize_row(raw)

    for col in ASSET_REQUIRED_COLUMNS:
        if get_cell(row, col) is None:
            return None, f"Row {row_num}: '{col}' is required"

    assetcode = str(get_cell(row, "assetcode")).strip()
    if db.query(Asset).filter(Asset.assetcode == assetcode).first():
        return None, f"Row {row_num}: assetcode '{assetcode}' already exists"

    assetname = str(get_cell(row, "assetname")).strip()

    try:
        def _resolve_table(model, id_field, name_field, val, ref_name):
            pid = parse_id_value(val)
            if pid is not None:
                obj = db.query(model).filter(getattr(model, id_field) == pid).first()
            else:
                obj = db.query(model).filter(getattr(model, name_field).ilike(str(val))).first()
            if not obj:
                raise ValueError(f"'{val}' not found — see {ref_name}")
            return getattr(obj, id_field)

        maincategoryid = _resolve_table(
            MainCategory, "maincategoryid", "categoryname",
            get_cell(row, "maincategoryid"), "ref_maincategories",
        )

        categoryid = None
        cv = get_cell(row, "categoryid")
        if cv is not None and str(cv).strip():
            cid = parse_id_value(cv)
            if cid is not None:
                cat = db.query(Category).filter(Category.id == cid).first()
            else:
                cat = db.query(Category).filter(Category.name.ilike(str(cv))).first()
            if not cat:
                return None, f"Row {row_num}: categoryid '{cv}' not found — see ref_categories"
            categoryid = cat.id

        countryid = _resolve_table(Country, "countryid", "countryname", get_cell(row, "countryid"), "ref_countries")
        provinceid = _resolve_table(Province, "provinceid", "provincename", get_cell(row, "provinceid"), "ref_provinces")
        companyid = _resolve_table(Company, "companyid", "companyname", get_cell(row, "companyid"), "ref_companies")
        locationid = _resolve_table(Location, "id", "name", get_cell(row, "locationid"), "ref_locations")

        company = db.query(Company).filter(Company.companyid == companyid).first()
        province = db.query(Province).filter(Province.provinceid == provinceid).first()
        if company and province and company.provinceid and company.provinceid != provinceid:
            return None, f"Row {row_num}: companyid {companyid} does not match provinceid {provinceid}"

        departmentid = None
        dv = get_cell(row, "departmentid")
        if dv is not None and str(dv).strip():
            departmentid = _resolve_table(Department, "departmentid", "departmentname", dv, "ref_departments")

        statusid = _resolve_table(AssetStatus, "statusid", "statusname", get_cell(row, "statusid"), "ref_assetstatuses")

        assignedto = None
        av = get_cell(row, "assignedto")
        if av is not None and str(av).strip():
            sid = parse_id_value(av)
            if sid is not None:
                st = db.query(Staff).filter(Staff.staffid == sid).first()
            else:
                st = db.query(Staff).filter(Staff.employeeid == str(av).strip()).first()
            if not st:
                return None, f"Row {row_num}: assignedto '{av}' not found — see ref_staff"
            assignedto = st.staffid

        createdby = current_user.userid
        cbv = get_cell(row, "createdby")
        if cbv is not None and str(cbv).strip():
            uid = parse_id_value(cbv)
            if uid is not None:
                u = db.query(User).filter(User.userid == uid).first()
            else:
                u = db.query(User).filter(User.email.ilike(str(cbv))).first()
            if u:
                createdby = u.userid

        stockid = None
        sv = get_cell(row, "stockid")
        if sv is not None and str(sv).strip():
            try:
                stockid = parse_stockid(sv)
            except ValueError as e:
                return None, f"Row {row_num}: stockid — {e}"

        now = datetime.utcnow()
        qrcode_val = get_cell(row, "qrcode")
        if not qrcode_val or len(str(qrcode_val)) < 20:
            qrcode_val = QRCodeService.generate_asset_qr(asset_id=assetcode, asset_name=assetname)

        asset = Asset(
            assetcode=assetcode,
            assetname=assetname,
            serialnumber=get_cell(row, "serialnumber"),
            modelnumber=get_cell(row, "modelnumber"),
            manufacturer=get_cell(row, "manufacturer"),
            maincategoryid=maincategoryid,
            categoryid=categoryid,
            countryid=countryid,
            provinceid=provinceid,
            companyid=companyid,
            locationid=locationid,
            departmentid=departmentid,
            assignedto=assignedto,
            assigneddate=_parse_date(get_cell(row, "assigneddate")),
            purchasedate=_parse_date(get_cell(row, "purchasedate")),
            purchaseprice=_parse_float(get_cell(row, "purchaseprice")),
            currentvalue=_parse_float(get_cell(row, "currentvalue")),
            depreciationrate=_parse_float(get_cell(row, "depreciationrate")),
            warrantyexpiry=_parse_date(get_cell(row, "warrantyexpiry")),
            po_number=get_cell(row, "ponumber") or get_cell(row, "po_number"),
            po_attachment_path=get_cell(row, "poattachmentpath") or get_cell(row, "po_attachment_path"),
            cost_center=get_cell(row, "costcenter") or get_cell(row, "cost_center"),
            statusid=statusid,
            condition=str(get_cell(row, "condition") or "Good"),
            specifications=get_cell(row, "specifications"),
            qrcode=str(qrcode_val) if qrcode_val else None,
            isactive=_parse_int_flag(get_cell(row, "isactive"), 1),
            createdat=_parse_date(get_cell(row, "createdat")) or now,
            updatedat=_parse_date(get_cell(row, "updatedat")) or now,
            createdby=createdby,
            notes=get_cell(row, "notes"),
            stockid=stockid,
        )
        return asset, None

    except ValueError as e:
        return None, f"Row {row_num}: {e}"
    except Exception as e:
        return None, f"Row {row_num}: {str(e)}"
