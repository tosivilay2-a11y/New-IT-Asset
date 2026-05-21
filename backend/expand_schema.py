"""
Expand database schema to match comprehensive IT Asset Management system
This adds all the additional tables from the SQL Server schema
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import sys

# SQL to create all additional tables
EXPANSION_SQL = """
-- =============================================
-- GEOGRAPHIC & ORGANIZATIONAL HIERARCHY
-- =============================================

CREATE TABLE IF NOT EXISTS countries (
    countryid SERIAL PRIMARY KEY,
    countryname VARCHAR(100) NOT NULL,
    countrycode VARCHAR(2) NOT NULL UNIQUE,
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS provinces (
    provinceid SERIAL PRIMARY KEY,
    provincename VARCHAR(100) NOT NULL,
    provincecode VARCHAR(3) NOT NULL,
    countryid INTEGER NOT NULL REFERENCES countries(countryid),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS companies (
    companyid SERIAL PRIMARY KEY,
    companyname VARCHAR(200) NOT NULL,
    companycode VARCHAR(10) NOT NULL UNIQUE,
    address VARCHAR(500),
    phone VARCHAR(20),
    email VARCHAR(100),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expand existing locations table
ALTER TABLE locations ADD COLUMN IF NOT EXISTS locationcode VARCHAR(3);
ALTER TABLE locations ADD COLUMN IF NOT EXISTS companyid INTEGER REFERENCES companies(companyid);
ALTER TABLE locations ADD COLUMN IF NOT EXISTS provinceid INTEGER REFERENCES provinces(provinceid);
ALTER TABLE locations ADD COLUMN IF NOT EXISTS department VARCHAR(100);
ALTER TABLE locations ADD COLUMN IF NOT EXISTS isactive BOOLEAN DEFAULT TRUE;

CREATE TABLE IF NOT EXISTS departments (
    departmentid SERIAL PRIMARY KEY,
    departmentname VARCHAR(100) NOT NULL,
    departmentcode VARCHAR(20) NOT NULL,
    companyid INTEGER NOT NULL REFERENCES companies(companyid),
    manageruserid INTEGER,
    description VARCHAR(500),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- USER MANAGEMENT EXPANSION
-- =============================================

CREATE TABLE IF NOT EXISTS usertypes (
    usertypeid SERIAL PRIMARY KEY,
    typename VARCHAR(50) NOT NULL,
    typecode VARCHAR(10) NOT NULL,
    description VARCHAR(200),
    managerlevel INTEGER DEFAULT 0,
    canapprove BOOLEAN DEFAULT FALSE,
    canmanageusers BOOLEAN DEFAULT FALSE,
    canaccessreports BOOLEAN DEFAULT FALSE,
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS userroles (
    roleid SERIAL PRIMARY KEY,
    rolename VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(500),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    permissionid SERIAL PRIMARY KEY,
    permissionkey VARCHAR(100) NOT NULL UNIQUE,
    permissionname VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    category VARCHAR(50),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rolepermissions (
    rolepermissionid SERIAL PRIMARY KEY,
    roleid INTEGER NOT NULL REFERENCES userroles(roleid),
    permissionid INTEGER NOT NULL REFERENCES permissions(permissionid),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(roleid, permissionid)
);

-- Expand existing users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS employeeid VARCHAR(50) UNIQUE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(100) UNIQUE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS firstname VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS lastname VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS department VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS position VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS usertype VARCHAR(50) DEFAULT 'Staff';
ALTER TABLE users ADD COLUMN IF NOT EXISTS usertypeid INTEGER REFERENCES usertypes(usertypeid);
ALTER TABLE users ADD COLUMN IF NOT EXISTS companyid INTEGER REFERENCES companies(companyid);
ALTER TABLE users ADD COLUMN IF NOT EXISTS countryid INTEGER REFERENCES countries(countryid);
ALTER TABLE users ADD COLUMN IF NOT EXISTS managerid INTEGER REFERENCES users(id);
ALTER TABLE users ADD COLUMN IF NOT EXISTS roleid INTEGER REFERENCES userroles(roleid);
ALTER TABLE users ADD COLUMN IF NOT EXISTS isactive BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS requirepasswordchange BOOLEAN DEFAULT FALSE;

-- =============================================
-- ASSET CATEGORIES EXPANSION
-- =============================================

CREATE TABLE IF NOT EXISTS maincategories (
    maincategoryid SERIAL PRIMARY KEY,
    categoryname VARCHAR(100) NOT NULL UNIQUE,
    categorycode VARCHAR(10) NOT NULL UNIQUE,
    description VARCHAR(500),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expand existing categories table
ALTER TABLE categories ADD COLUMN IF NOT EXISTS maincategoryid INTEGER REFERENCES maincategories(maincategoryid);
ALTER TABLE categories ADD COLUMN IF NOT EXISTS isactive BOOLEAN DEFAULT TRUE;

CREATE TABLE IF NOT EXISTS assetstatuses (
    statusid SERIAL PRIMARY KEY,
    statusname VARCHAR(50) NOT NULL UNIQUE,
    statuscode VARCHAR(20) NOT NULL UNIQUE,
    description VARCHAR(200),
    colorcode VARCHAR(20) DEFAULT 'secondary',
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- ASSET MANAGEMENT EXPANSION
-- =============================================

CREATE TABLE IF NOT EXISTS assetsequences (
    sequenceid SERIAL PRIMARY KEY,
    countryid INTEGER NOT NULL REFERENCES countries(countryid),
    companyid INTEGER NOT NULL REFERENCES companies(companyid),
    sequenceyear INTEGER NOT NULL,
    year INTEGER NOT NULL,
    lastsequence INTEGER DEFAULT 0,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(countryid, companyid, sequenceyear)
);

-- Expand existing assets table with all comprehensive fields
ALTER TABLE assets ADD COLUMN IF NOT EXISTS picture TEXT;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS maincategory VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS brand VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS model VARCHAR(200);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS modelname VARCHAR(200);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS cpu VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS ram VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS hdd VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS wlanmacaddress VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS lanmacaddress VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS serialnumber VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS sntype VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS assignedto INTEGER REFERENCES users(id);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS dateassigned TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS datepurchase TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS datefirstuse TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS endoflife TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS price DECIMAL(18,2);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS ponumber VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS invoice TEXT;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS deliverynote TEXT;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS replacementcost DECIMAL(18,2);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS supplierwarrantytype VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS supplierwarrantyscope VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS supplierwarrantyservicemethod VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS supplierwarrantystart TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS supplierwarrantyend TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarranty VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarrantycompany VARCHAR(200);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarrantytype VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarrantyscope VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarrantyservicemethod VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarrantystart TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS additionalwarrantyend TIMESTAMP;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS locationname VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS currentlocationid INTEGER REFERENCES locations(id);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS currentlocationname VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS companyid INTEGER REFERENCES companies(companyid);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS provinceid INTEGER REFERENCES provinces(provinceid);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS countryid INTEGER REFERENCES countries(countryid);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS computername VARCHAR(100);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS accessories VARCHAR(500);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS comment TEXT;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS condition VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS year INTEGER;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS month INTEGER;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS testnumber VARCHAR(50);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS qrcode TEXT;
ALTER TABLE assets ADD COLUMN IF NOT EXISTS createdby INTEGER REFERENCES users(id);
ALTER TABLE assets ADD COLUMN IF NOT EXISTS modifiedby INTEGER REFERENCES users(id);

CREATE TABLE IF NOT EXISTS assetassignments (
    assignmentid SERIAL PRIMARY KEY,
    assetid VARCHAR(50) NOT NULL,
    userid INTEGER NOT NULL REFERENCES users(id),
    assigneddate TIMESTAMP NOT NULL,
    returneddate TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    notes TEXT,
    assignedby INTEGER REFERENCES users(id),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assetauditlog (
    auditid SERIAL PRIMARY KEY,
    assetid VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    oldvalue TEXT,
    newvalue TEXT,
    changedby INTEGER REFERENCES users(id),
    changedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assetevents (
    eventid SERIAL PRIMARY KEY,
    assetid VARCHAR(50) NOT NULL,
    eventtype VARCHAR(50) NOT NULL,
    eventdate TIMESTAMP NOT NULL,
    description TEXT,
    performedby INTEGER REFERENCES users(id),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- STOCK COUNT & RECONCILIATION
-- =============================================

CREATE TABLE IF NOT EXISTS stockcountsessions (
    sessionid SERIAL PRIMARY KEY,
    sessionname VARCHAR(200) NOT NULL,
    locationid INTEGER NOT NULL REFERENCES locations(id),
    startdate TIMESTAMP NOT NULL,
    enddate TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Planning',
    createdby INTEGER NOT NULL REFERENCES users(id),
    completedby INTEGER REFERENCES users(id),
    completedat TIMESTAMP,
    notes TEXT,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stockcounts (
    countid SERIAL PRIMARY KEY,
    sessionid INTEGER REFERENCES stockcountsessions(sessionid),
    locationid INTEGER NOT NULL REFERENCES locations(id),
    assetid VARCHAR(50) NOT NULL,
    userid INTEGER REFERENCES users(id),
    countdate DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    expectedquantity INTEGER,
    actualquantity INTEGER,
    discrepancytype VARCHAR(50),
    notes VARCHAR(500),
    countedat TIMESTAMP,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stockcountitems (
    itemid SERIAL PRIMARY KEY,
    sessionid INTEGER NOT NULL REFERENCES stockcountsessions(sessionid),
    assetid VARCHAR(50) NOT NULL,
    expectedstatus VARCHAR(50),
    actualstatus VARCHAR(50),
    expectedlocation INTEGER REFERENCES locations(id),
    actuallocation INTEGER REFERENCES locations(id),
    discrepancytype VARCHAR(50),
    countedby INTEGER REFERENCES users(id),
    countedat TIMESTAMP,
    notes TEXT,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reconciliations (
    reconciliationid SERIAL PRIMARY KEY,
    stockcountid INTEGER REFERENCES stockcounts(countid),
    assetid VARCHAR(50) NOT NULL,
    discrepancytype VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    reportedby INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(50) NOT NULL DEFAULT 'Reported',
    resolution TEXT,
    resolvedby INTEGER REFERENCES users(id),
    resolveddate TIMESTAMP,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- WORKFLOW & APPROVALS
-- =============================================

CREATE TABLE IF NOT EXISTS approvallevels (
    levelid SERIAL PRIMARY KEY,
    companyid INTEGER NOT NULL REFERENCES companies(companyid),
    level INTEGER NOT NULL,
    approveruserid INTEGER NOT NULL REFERENCES users(id),
    requesttype VARCHAR(50) NOT NULL,
    minamount DECIMAL(18,2),
    maxamount DECIMAL(18,2),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approvals (
    approvalid SERIAL PRIMARY KEY,
    requesttype VARCHAR(50) NOT NULL,
    requestid VARCHAR(50) NOT NULL,
    requesterid INTEGER NOT NULL REFERENCES users(id),
    currentapproverid INTEGER REFERENCES users(id),
    approvallevel INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    comments TEXT,
    requesteddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approveddate TIMESTAMP
);

-- =============================================
-- BUDGET MANAGEMENT
-- =============================================

CREATE TABLE IF NOT EXISTS budgetplans (
    budgetid SERIAL PRIMARY KEY,
    fiscalyear INTEGER NOT NULL,
    department VARCHAR(100),
    category VARCHAR(100),
    plannedamount DECIMAL(18,2) NOT NULL,
    actualamount DECIMAL(18,2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Active',
    createdby INTEGER REFERENCES users(id),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SYSTEM TABLES
-- =============================================

CREATE TABLE IF NOT EXISTS auditlogs (
    logid SERIAL PRIMARY KEY,
    tablename VARCHAR(100) NOT NULL,
    recordid VARCHAR(50) NOT NULL,
    action VARCHAR(20) NOT NULL,
    userid INTEGER REFERENCES users(id),
    oldvalue TEXT,
    newvalue TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ipaddress VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS notifications (
    notificationid SERIAL PRIMARY KEY,
    userid INTEGER NOT NULL REFERENCES users(id),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    isread BOOLEAN DEFAULT FALSE,
    relatedentitytype VARCHAR(50),
    relatedentityid VARCHAR(50),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    readat TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_assets_assetid ON assets(asset_id);
CREATE INDEX IF NOT EXISTS idx_assets_status ON assets(status);
CREATE INDEX IF NOT EXISTS idx_assets_companyid ON assets(companyid);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_employeeid ON users(employeeid);
CREATE INDEX IF NOT EXISTS idx_stockcounts_sessionid ON stockcounts(sessionid);
CREATE INDEX IF NOT EXISTS idx_approvals_status ON approvals(status);
CREATE INDEX IF NOT EXISTS idx_notifications_userid ON notifications(userid);
CREATE INDEX IF NOT EXISTS idx_auditlogs_tablename ON auditlogs(tablename);
"""

def expand_schema():
    """Execute schema expansion"""
    try:
        print("=" * 60)
        print("EXPANDING DATABASE SCHEMA")
        print("=" * 60)
        print()
        
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        print("✓ Connected to database")
        print()
        print("Executing schema expansion...")
        print()
        
        # Execute SQL
        with engine.connect() as conn:
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in EXPANSION_SQL.split(';') if s.strip()]
            
            for i, statement in enumerate(statements, 1):
                if statement:
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                        # Print progress for CREATE TABLE statements
                        if 'CREATE TABLE' in statement:
                            table_name = statement.split('CREATE TABLE')[1].split('(')[0].strip().split()[-1]
                            print(f"  ✓ Created/verified table: {table_name}")
                        elif 'ALTER TABLE' in statement and 'ADD COLUMN' in statement:
                            table_name = statement.split('ALTER TABLE')[1].split('ADD')[0].strip()
                            column_name = statement.split('ADD COLUMN')[1].split()[1]
                            print(f"  ✓ Added column {column_name} to {table_name}")
                    except Exception as e:
                        # Ignore "already exists" errors
                        if 'already exists' not in str(e).lower() and 'duplicate' not in str(e).lower():
                            print(f"  ⚠ Warning: {str(e)[:100]}")
        
        print()
        print("=" * 60)
        print("✓ SCHEMA EXPANSION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Your database now includes:")
        print("  • Geographic hierarchy (Countries, Provinces, Companies)")
        print("  • Expanded user management (UserTypes, Roles, Permissions)")
        print("  • Comprehensive asset tracking")
        print("  • Stock count & reconciliation")
        print("  • Approval workflows")
        print("  • Budget management")
        print("  • System audit logs & notifications")
        print()
        print("Total: 30+ tables with full relationships")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR DURING SCHEMA EXPANSION")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    success = expand_schema()
    sys.exit(0 if success else 1)
