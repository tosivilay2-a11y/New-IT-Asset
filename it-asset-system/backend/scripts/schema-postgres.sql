-- =============================================
-- IT Asset Management System - Database Schema
-- PostgreSQL 12+
-- =============================================

-- Note: Database it_asset_db is created by Docker
-- This script runs automatically on container initialization

-- =============================================
-- 1. GEOGRAPHIC & ORGANIZATIONAL HIERARCHY
-- =============================================

-- Countries Table
CREATE TABLE IF NOT EXISTS Countries (
    CountryID SERIAL PRIMARY KEY,
    CountryName VARCHAR(100) NOT NULL,
    CountryCode VARCHAR(2) NOT NULL UNIQUE,
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Provinces Table
CREATE TABLE IF NOT EXISTS Provinces (
    ProvinceID SERIAL PRIMARY KEY,
    ProvinceName VARCHAR(100) NOT NULL,
    ProvinceCode VARCHAR(3) NOT NULL,
    CountryID INTEGER NOT NULL REFERENCES Countries(CountryID),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies Table
CREATE TABLE IF NOT EXISTS Companies (
    CompanyID SERIAL PRIMARY KEY,
    CompanyName VARCHAR(200) NOT NULL,
    CompanyCode VARCHAR(10) NOT NULL UNIQUE,
    Address VARCHAR(500),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Locations Table
CREATE TABLE IF NOT EXISTS Locations (
    LocationID SERIAL PRIMARY KEY,
    LocationName VARCHAR(200) NOT NULL,
    LocationCode VARCHAR(3) NOT NULL,
    CompanyID INTEGER REFERENCES Companies(CompanyID),
    ProvinceID INTEGER REFERENCES Provinces(ProvinceID),
    Address VARCHAR(500),
    Department VARCHAR(100),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Departments Table
CREATE TABLE IF NOT EXISTS Departments (
    DepartmentID SERIAL PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL,
    DepartmentCode VARCHAR(20) NOT NULL,
    CompanyID INTEGER NOT NULL REFERENCES Companies(CompanyID),
    ManagerUserID INTEGER,
    Description VARCHAR(500),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 2. USER MANAGEMENT & AUTHENTICATION
-- =============================================

-- UserTypes Table
CREATE TABLE IF NOT EXISTS UserTypes (
    UserTypeID SERIAL PRIMARY KEY,
    TypeName VARCHAR(50) NOT NULL,
    TypeCode VARCHAR(10) NOT NULL,
    Description VARCHAR(200),
    ManagerLevel INTEGER DEFAULT 0,
    CanApprove BOOLEAN DEFAULT FALSE,
    CanManageUsers BOOLEAN DEFAULT FALSE,
    CanAccessReports BOOLEAN DEFAULT FALSE,
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    UserID SERIAL PRIMARY KEY,
    EmployeeID VARCHAR(50) NOT NULL UNIQUE,
    Username VARCHAR(100) NOT NULL UNIQUE,
    Email VARCHAR(200) NOT NULL,
    Password VARCHAR(255),
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Department VARCHAR(100),
    Position VARCHAR(100),
    UserType VARCHAR(50) NOT NULL DEFAULT 'Staff',
    UserTypeID INTEGER REFERENCES UserTypes(UserTypeID),
    CompanyID INTEGER REFERENCES Companies(CompanyID),
    CountryID INTEGER REFERENCES Countries(CountryID),
    ManagerID INTEGER REFERENCES Users(UserID),
    RoleID INTEGER,
    IsActive BOOLEAN DEFAULT TRUE,
    RequirePasswordChange BOOLEAN DEFAULT FALSE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UserRoles Table
CREATE TABLE IF NOT EXISTS UserRoles (
    RoleID SERIAL PRIMARY KEY,
    RoleName VARCHAR(100) NOT NULL UNIQUE,
    Description VARCHAR(500),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permissions Table
CREATE TABLE IF NOT EXISTS Permissions (
    PermissionID SERIAL PRIMARY KEY,
    PermissionKey VARCHAR(100) NOT NULL UNIQUE,
    PermissionName VARCHAR(100) NOT NULL,
    Description VARCHAR(500),
    Category VARCHAR(50),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RolePermissions Junction Table
CREATE TABLE IF NOT EXISTS RolePermissions (
    RolePermissionID SERIAL PRIMARY KEY,
    RoleID INTEGER NOT NULL REFERENCES UserRoles(RoleID),
    PermissionID INTEGER NOT NULL REFERENCES Permissions(PermissionID),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(RoleID, PermissionID)
);

-- =============================================
-- 3. ASSET CATEGORIES & CONFIGURATION
-- =============================================

-- MainCategories Table
CREATE TABLE IF NOT EXISTS MainCategories (
    MainCategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE,
    CategoryCode VARCHAR(10) NOT NULL UNIQUE,
    Description VARCHAR(500),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE IF NOT EXISTS Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL,
    MainCategoryID INTEGER NOT NULL REFERENCES MainCategories(MainCategoryID),
    Description VARCHAR(500),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AssetStatuses Table
CREATE TABLE IF NOT EXISTS AssetStatuses (
    StatusID SERIAL PRIMARY KEY,
    StatusName VARCHAR(50) NOT NULL UNIQUE,
    StatusCode VARCHAR(20) NOT NULL UNIQUE,
    Description VARCHAR(200),
    ColorCode VARCHAR(20) DEFAULT 'secondary',
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 4. ASSET MANAGEMENT
-- =============================================

-- AssetSequences Table (for ID generation)
CREATE TABLE IF NOT EXISTS AssetSequences (
    SequenceID SERIAL PRIMARY KEY,
    CountryID INTEGER NOT NULL REFERENCES Countries(CountryID),
    CompanyID INTEGER NOT NULL REFERENCES Companies(CompanyID),
    SequenceYear INTEGER NOT NULL,
    Year INTEGER NOT NULL,
    LastSequence INTEGER DEFAULT 0,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(CountryID, CompanyID, SequenceYear)
);

-- Assets Table
CREATE TABLE IF NOT EXISTS Assets (
    AssetID VARCHAR(50) PRIMARY KEY,
    Picture TEXT,
    MainCategory VARCHAR(100) NOT NULL,
    Status VARCHAR(50) NOT NULL DEFAULT 'Available',
    Category VARCHAR(100),
    ModelName VARCHAR(200),
    Brand VARCHAR(100),
    Model VARCHAR(200),
    CPU VARCHAR(100),
    Ram VARCHAR(50),
    HDD VARCHAR(50),
    WLANMACAddress VARCHAR(50),
    LANMACAddress VARCHAR(50),
    Description TEXT,
    SerialNumber VARCHAR(100),
    SNType VARCHAR(50),
    
    -- Assignment
    AssignedTo INTEGER REFERENCES Users(UserID),
    Department VARCHAR(100),
    DateAssigned TIMESTAMP,
    
    -- Purchase Information
    DatePurchase TIMESTAMP,
    DateFirstUse TIMESTAMP,
    EndOfLife TIMESTAMP,
    Price DECIMAL(18,2),
    PONumber VARCHAR(50),
    Invoice TEXT,
    DeliveryNote TEXT,
    ReplacementCost DECIMAL(18,2),
    
    -- Warranty Information
    SupplierWarrantyType VARCHAR(100),
    SupplierWarrantyScope VARCHAR(100),
    SupplierWarrantyServiceMethod VARCHAR(100),
    SupplierWarrantyStart TIMESTAMP,
    SupplierWarrantyEnd TIMESTAMP,
    AdditionalWarranty VARCHAR(100),
    AdditionalWarrantyCompany VARCHAR(200),
    AdditionalWarrantyType VARCHAR(100),
    AdditionalWarrantyScope VARCHAR(100),
    AdditionalWarrantyServiceMethod VARCHAR(100),
    AdditionalWarrantyStart TIMESTAMP,
    AdditionalWarrantyEnd TIMESTAMP,
    
    -- Location Information
    LocationID INTEGER REFERENCES Locations(LocationID),
    LocationName VARCHAR(100),
    CurrentLocationID INTEGER REFERENCES Locations(LocationID),
    CurrentLocationName VARCHAR(100),
    CompanyID INTEGER REFERENCES Companies(CompanyID),
    ProvinceID INTEGER REFERENCES Provinces(ProvinceID),
    CountryID INTEGER REFERENCES Countries(CountryID),
    
    -- Additional Fields
    ComputerName VARCHAR(100),
    Accessories VARCHAR(500),
    Comment TEXT,
    Condition VARCHAR(50),
    Year INTEGER,
    Month INTEGER,
    TestNumber VARCHAR(50),
    QRCode TEXT,
    
    -- Audit Fields
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER REFERENCES Users(UserID),
    ModifiedBy INTEGER REFERENCES Users(UserID)
);

-- AssetAssignments Table (History)
CREATE TABLE IF NOT EXISTS AssetAssignments (
    AssignmentID SERIAL PRIMARY KEY,
    AssetID VARCHAR(50) NOT NULL REFERENCES Assets(AssetID),
    UserID INTEGER NOT NULL REFERENCES Users(UserID),
    AssignedDate TIMESTAMP NOT NULL,
    ReturnedDate TIMESTAMP,
    Status VARCHAR(50) NOT NULL DEFAULT 'Active',
    Notes TEXT,
    AssignedBy INTEGER REFERENCES Users(UserID),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AssetAuditLog Table
CREATE TABLE IF NOT EXISTS AssetAuditLog (
    AuditID SERIAL PRIMARY KEY,
    AssetID VARCHAR(50) NOT NULL REFERENCES Assets(AssetID),
    Action VARCHAR(50) NOT NULL,
    OldValue TEXT,
    NewValue TEXT,
    ChangedBy INTEGER REFERENCES Users(UserID),
    ChangedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AssetEvents Table
CREATE TABLE IF NOT EXISTS AssetEvents (
    EventID SERIAL PRIMARY KEY,
    AssetID VARCHAR(50) NOT NULL REFERENCES Assets(AssetID),
    EventType VARCHAR(50) NOT NULL,
    EventDate TIMESTAMP NOT NULL,
    Description TEXT,
    PerformedBy INTEGER REFERENCES Users(UserID),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 5. STOCK COUNT & RECONCILIATION
-- =============================================

-- StockCountSessions Table
CREATE TABLE IF NOT EXISTS StockCountSessions (
    SessionID SERIAL PRIMARY KEY,
    SessionName VARCHAR(200) NOT NULL,
    LocationID INTEGER NOT NULL REFERENCES Locations(LocationID),
    StartDate TIMESTAMP NOT NULL,
    EndDate TIMESTAMP,
    Status VARCHAR(50) NOT NULL DEFAULT 'Planning',
    CreatedBy INTEGER NOT NULL REFERENCES Users(UserID),
    CompletedBy INTEGER REFERENCES Users(UserID),
    CompletedAt TIMESTAMP,
    Notes TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- StockCounts Table
CREATE TABLE IF NOT EXISTS StockCounts (
    CountID SERIAL PRIMARY KEY,
    SessionID INTEGER REFERENCES StockCountSessions(SessionID),
    LocationID INTEGER NOT NULL REFERENCES Locations(LocationID),
    AssetID VARCHAR(50) NOT NULL REFERENCES Assets(AssetID),
    UserID INTEGER REFERENCES Users(UserID),
    CountDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    ExpectedQuantity INTEGER,
    ActualQuantity INTEGER,
    DiscrepancyType VARCHAR(50),
    Notes VARCHAR(500),
    CountedAt TIMESTAMP,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- StockCountItems Table
CREATE TABLE IF NOT EXISTS StockCountItems (
    ItemID SERIAL PRIMARY KEY,
    SessionID INTEGER NOT NULL REFERENCES StockCountSessions(SessionID),
    AssetID VARCHAR(50) NOT NULL REFERENCES Assets(AssetID),
    ExpectedStatus VARCHAR(50),
    ActualStatus VARCHAR(50),
    ExpectedLocation INTEGER,
    ActualLocation INTEGER,
    DiscrepancyType VARCHAR(50),
    CountedBy INTEGER REFERENCES Users(UserID),
    CountedAt TIMESTAMP,
    Notes TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reconciliations Table (Discrepancy Resolution)
CREATE TABLE IF NOT EXISTS Reconciliations (
    ReconciliationID SERIAL PRIMARY KEY,
    StockCountID INTEGER REFERENCES StockCounts(CountID),
    AssetID VARCHAR(50) NOT NULL REFERENCES Assets(AssetID),
    DiscrepancyType VARCHAR(50) NOT NULL,
    Description TEXT NOT NULL,
    ReportedBy INTEGER NOT NULL REFERENCES Users(UserID),
    Status VARCHAR(50) NOT NULL DEFAULT 'Reported',
    Resolution TEXT,
    ResolvedBy INTEGER REFERENCES Users(UserID),
    ResolvedDate TIMESTAMP,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 6. WORKFLOW & APPROVALS
-- =============================================

-- ApprovalLevels Configuration Table
CREATE TABLE IF NOT EXISTS ApprovalLevels (
    LevelID SERIAL PRIMARY KEY,
    CompanyID INTEGER NOT NULL REFERENCES Companies(CompanyID),
    Level INTEGER NOT NULL,
    ApproverUserID INTEGER NOT NULL REFERENCES Users(UserID),
    RequestType VARCHAR(50) NOT NULL,
    MinAmount DECIMAL(18,2),
    MaxAmount DECIMAL(18,2),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approvals Table
CREATE TABLE IF NOT EXISTS Approvals (
    ApprovalID SERIAL PRIMARY KEY,
    RequestType VARCHAR(50) NOT NULL,
    RequestID VARCHAR(50) NOT NULL,
    RequesterID INTEGER NOT NULL REFERENCES Users(UserID),
    CurrentApproverID INTEGER REFERENCES Users(UserID),
    ApprovalLevel INTEGER NOT NULL DEFAULT 1,
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    Comments TEXT,
    RequestedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ApprovedDate TIMESTAMP
);

-- =============================================
-- 7. BUDGET MANAGEMENT
-- =============================================

-- BudgetPlans Table
CREATE TABLE IF NOT EXISTS BudgetPlans (
    BudgetID SERIAL PRIMARY KEY,
    FiscalYear INTEGER NOT NULL,
    Department VARCHAR(100),
    Category VARCHAR(100),
    PlannedAmount DECIMAL(18,2) NOT NULL,
    ActualAmount DECIMAL(18,2) DEFAULT 0,
    Status VARCHAR(50) DEFAULT 'Active',
    CreatedBy INTEGER REFERENCES Users(UserID),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 8. SYSTEM TABLES
-- =============================================

-- AuditLogs Table (System-wide)
CREATE TABLE IF NOT EXISTS AuditLogs (
    LogID SERIAL PRIMARY KEY,
    TableName VARCHAR(100) NOT NULL,
    RecordID VARCHAR(50) NOT NULL,
    Action VARCHAR(20) NOT NULL,
    UserID INTEGER REFERENCES Users(UserID),
    OldValue TEXT,
    NewValue TEXT,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IPAddress VARCHAR(50)
);

-- Notifications Table
CREATE TABLE IF NOT EXISTS Notifications (
    NotificationID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL REFERENCES Users(UserID),
    Type VARCHAR(50) NOT NULL,
    Title VARCHAR(200) NOT NULL,
    Message TEXT NOT NULL,
    IsRead BOOLEAN DEFAULT FALSE,
    RelatedEntityType VARCHAR(50),
    RelatedEntityID VARCHAR(50),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ReadAt TIMESTAMP
);

-- =============================================
-- CREATE INDEXES FOR PERFORMANCE
-- =============================================

CREATE INDEX IF NOT EXISTS idx_provinces_country ON Provinces(CountryID);
CREATE INDEX IF NOT EXISTS idx_locations_company ON Locations(CompanyID);
CREATE INDEX IF NOT EXISTS idx_locations_province ON Locations(ProvinceID);
CREATE INDEX IF NOT EXISTS idx_users_email ON Users(Email);
CREATE INDEX IF NOT EXISTS idx_users_username ON Users(Username);
CREATE INDEX IF NOT EXISTS idx_users_company ON Users(CompanyID);
CREATE INDEX IF NOT EXISTS idx_rolepermissions_role ON RolePermissions(RoleID);
CREATE INDEX IF NOT EXISTS idx_rolepermissions_permission ON RolePermissions(PermissionID);
CREATE INDEX IF NOT EXISTS idx_assets_status ON Assets(Status);
CREATE INDEX IF NOT EXISTS idx_assets_location ON Assets(LocationID);
CREATE INDEX IF NOT EXISTS idx_assets_company ON Assets(CompanyID);
CREATE INDEX IF NOT EXISTS idx_assets_assigned ON Assets(AssignedTo);
CREATE INDEX IF NOT EXISTS idx_assetassignments_asset ON AssetAssignments(AssetID);
CREATE INDEX IF NOT EXISTS idx_assetassignments_user ON AssetAssignments(UserID);
CREATE INDEX IF NOT EXISTS idx_assetauditlog_asset ON AssetAuditLog(AssetID);
CREATE INDEX IF NOT EXISTS idx_stockcounts_session ON StockCounts(SessionID);
CREATE INDEX IF NOT EXISTS idx_stockcounts_asset ON StockCounts(AssetID);
CREATE INDEX IF NOT EXISTS idx_auditlogs_table ON AuditLogs(TableName, RecordID);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON Notifications(UserID);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON Notifications(IsRead);

-- Print success message
DO $$
BEGIN
    RAISE NOTICE 'All tables and indexes created successfully!';
    RAISE NOTICE 'Total tables: 30';
END $$;
