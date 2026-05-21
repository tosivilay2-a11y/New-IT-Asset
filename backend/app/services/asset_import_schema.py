"""
Asset batch import — exact `public.assets` column layout (matches DB SELECT order).
Reference sheets supply valid IDs; Excel dropdowns on FK columns use "id - label" lists.
"""
from typing import Dict, List, Tuple

# Excludes assetid (auto). Order matches: SELECT ... FROM public.assets
ASSET_DB_COLUMNS: List[str] = [
    "assetcode",
    "assetname",
    "serialnumber",
    "modelnumber",
    "manufacturer",
    "maincategoryid",
    "categoryid",
    "countryid",
    "provinceid",
    "companyid",
    "locationid",
    "departmentid",
    "assignedto",
    "assigneddate",
    "purchasedate",
    "purchaseprice",
    "currentvalue",
    "depreciationrate",
    "warrantyexpiry",
    "po_number",
    "po_attachment_path",
    "cost_center",
    "statusid",
    "condition",
    "specifications",
    "qrcode",
    "isactive",
    "createdat",
    "updatedat",
    "createdby",
    "notes",
    "stockid",
]

# Required for a new row (IDs or dropdown values)
ASSET_REQUIRED_COLUMNS = {
    "assetcode",
    "assetname",
    "maincategoryid",
    "countryid",
    "provinceid",
    "companyid",
    "locationid",
    "statusid",
}

# Import column index (1-based) -> reference sheet for dropdown (column C = list values)
FK_DROPDOWN_COLUMNS: Dict[str, Tuple[int, str]] = {
    "maincategoryid": (6, "ref_maincategories"),
    "categoryid": (7, "ref_categories"),
    "countryid": (8, "ref_countries"),
    "provinceid": (9, "ref_provinces"),
    "companyid": (10, "ref_companies"),
    "locationid": (11, "ref_locations"),
    "departmentid": (12, "ref_departments"),
    "assignedto": (13, "ref_staff"),
    "statusid": (23, "ref_assetstatuses"),
    "createdby": (30, "ref_users"),
    "stockid": (32, "ref_stocklocation"),
}

# Reference sheet definitions: (sheet_name, headers, id_field_name for docs)
REF_SHEET_SPECS = [
    ("ref_maincategories", ["maincategoryid", "categoryname", "categorycode", "pick_list"]),
    ("ref_categories", ["categoryid", "name", "pick_list"]),
    ("ref_countries", ["countryid", "countryname", "countrycode", "pick_list"]),
    ("ref_provinces", ["provinceid", "provincename", "provincecode", "countryid", "pick_list"]),
    ("ref_companies", ["companyid", "companyname", "companycode", "provinceid", "pick_list"]),
    ("ref_locations", ["locationid", "name", "companyid", "pick_list"]),
    ("ref_departments", ["departmentid", "departmentname", "departmentcode", "companyid", "pick_list"]),
    ("ref_assetstatuses", ["statusid", "statusname", "statuscode", "pick_list"]),
    ("ref_staff", ["staffid", "employeeid", "fullname", "pick_list"]),
    ("ref_stocklocation", ["stockid", "stockname", "locationid", "pick_list"]),
    ("ref_users", ["userid", "email", "pick_list"]),
]

INSTRUCTIONS_ROWS = [
    ["ASSET BATCH IMPORT — READ FIRST"],
    [""],
    ["1. Fill data on the 'Import' sheet using EXACT column names from the database."],
    ["2. For ID columns, pick from the dropdown OR copy the numeric ID from the matching ref_* sheet."],
    ["3. assetcode = your existing code (required). assetid is NOT imported (auto-generated)."],
    ["4. stockid = one stockid number, or comma-separated e.g. 3,4"],
    ["5. specifications = JSON text or plain text"],
    ["6. createdat / updatedat — leave blank to use import time"],
    [""],
    ["Column", "DB field", "Reference sheet"],
    ["assetcode", "assetcode", "—"],
    ["maincategoryid", "maincategoryid", "ref_maincategories"],
    ["categoryid", "categoryid", "ref_categories"],
    ["countryid", "countryid", "ref_countries"],
    ["provinceid", "provinceid", "ref_provinces"],
    ["companyid", "companyid", "ref_companies"],
    ["locationid", "locationid", "ref_locations"],
    ["departmentid", "departmentid", "ref_departments"],
    ["statusid", "statusid", "ref_assetstatuses"],
    ["assignedto", "assignedto (staffid)", "ref_staff"],
    ["stockid", "stockid", "ref_stocklocation"],
    ["createdby", "createdby (userid)", "ref_users"],
]
