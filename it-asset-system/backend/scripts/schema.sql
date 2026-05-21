-- =============================================
-- IT Asset Management System - Database Schema
-- SQL Server 2019+
-- =============================================

USE master;
GO

-- Create database if not exists
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'ITAssetManagement')
BEGIN
    CREATE DATABASE ITAssetManagement;
    PRINT 'Database ITAssetManagement created successfully';
END
ELSE
BEGIN
    PRINT 'Database ITAssetManagement already exists';
END
GO

USE ITAssetManagement;
GO

-- =============================================
-- 1. GEOGRAPHIC & ORGANIZATIONAL HIERARCHY
-- =============================================

-- Countries Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Countries')
BEGIN
    CREATE TABLE Countries (
        CountryID INT IDENTITY(1,1) PRIMARY KEY,
        CountryName NVARCHAR(100) NOT NULL,
        CountryCode NVARCHAR(2) NOT NULL UNIQUE,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table Countries created';
END
GO

-- Provinces Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Provinces')
BEGIN
    CREATE TABLE Provinces (
        ProvinceID INT IDENTITY(1,1) PRIMARY KEY,
        ProvinceName NVARCHAR(100) NOT NULL,
        ProvinceCode NVARCHAR(3) NOT NULL,
        CountryID INT NOT NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Provinces_Countries FOREIGN KEY (CountryID) REFERENCES Countries(CountryID)
    );
    PRINT 'Table Provinces created';
END
GO

-- Companies Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Companies')
BEGIN
    CREATE TABLE Companies (
        CompanyID INT IDENTITY(1,1) PRIMARY KEY,
        CompanyName NVARCHAR(200) NOT NULL,
        CompanyCode NVARCHAR(10) NOT NULL UNIQUE,
        Address NVARCHAR(500) NULL,
        Phone NVARCHAR(20) NULL,
        Email NVARCHAR(100) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table Companies created';
END
GO

-- Locations Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Locations')
BEGIN
    CREATE TABLE Locations (
        LocationID INT IDENTITY(1,1) PRIMARY KEY,
        LocationName NVARCHAR(200) NOT NULL,
        LocationCode NVARCHAR(3) NOT NULL,
        CompanyID INT NULL,
        ProvinceID INT NULL,
        Address NVARCHAR(500) NULL,
        Department NVARCHAR(100) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Locations_Companies FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
        CONSTRAINT FK_Locations_Provinces FOREIGN KEY (ProvinceID) REFERENCES Provinces(ProvinceID)
    );
    PRINT 'Table Locations created';
END
GO

-- Departments Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Departments')
BEGIN
    CREATE TABLE Departments (
        DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
        DepartmentName NVARCHAR(100) NOT NULL,
        DepartmentCode NVARCHAR(20) NOT NULL,
        CompanyID INT NOT NULL,
        ManagerUserID INT NULL,
        Description NVARCHAR(500) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Departments_Companies FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
    );
    PRINT 'Table Departments created';
END
GO

-- =============================================
-- 2. USER MANAGEMENT & AUTHENTICATION
-- =============================================

-- UserTypes Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'UserTypes')
BEGIN
    CREATE TABLE UserTypes (
        UserTypeID INT IDENTITY(1,1) PRIMARY KEY,
        TypeName NVARCHAR(50) NOT NULL,
        TypeCode NVARCHAR(10) NOT NULL,
        Description NVARCHAR(200) NULL,
        ManagerLevel INT DEFAULT 0,
        CanApprove BIT DEFAULT 0,
        CanManageUsers BIT DEFAULT 0,
        CanAccessReports BIT DEFAULT 0,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table UserTypes created';
END
GO

-- Users Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        EmployeeID NVARCHAR(50) NOT NULL UNIQUE,
        Username NVARCHAR(100) NOT NULL UNIQUE,
        Email NVARCHAR(200) NOT NULL,
        Password NVARCHAR(255) NULL,
        FirstName NVARCHAR(100) NULL,
        LastName NVARCHAR(100) NULL,
        Department NVARCHAR(100) NULL,
        Position NVARCHAR(100) NULL,
        UserType NVARCHAR(50) NOT NULL DEFAULT 'Staff',
        UserTypeID INT NULL,
        CompanyID INT NULL,
        CountryID INT NULL,
        ManagerID INT NULL,
        RoleID INT NULL,
        IsActive BIT DEFAULT 1,
        RequirePasswordChange BIT DEFAULT 0,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Users_UserTypes FOREIGN KEY (UserTypeID) REFERENCES UserTypes(UserTypeID),
        CONSTRAINT FK_Users_Companies FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
        CONSTRAINT FK_Users_Countries FOREIGN KEY (CountryID) REFERENCES Countries(CountryID),
        CONSTRAINT FK_Users_Manager FOREIGN KEY (ManagerID) REFERENCES Users(UserID)
    );
    PRINT 'Table Users created';
END
GO

-- Roles Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'UserRoles')
BEGIN
    CREATE TABLE UserRoles (
        RoleID INT IDENTITY(1,1) PRIMARY KEY,
        RoleName NVARCHAR(100) NOT NULL UNIQUE,
        Description NVARCHAR(500) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table UserRoles created';
END
GO

-- Permissions Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Permissions')
BEGIN
    CREATE TABLE Permissions (
        PermissionID INT IDENTITY(1,1) PRIMARY KEY,
        PermissionKey NVARCHAR(100) NOT NULL UNIQUE,
        PermissionName NVARCHAR(100) NOT NULL,
        Description NVARCHAR(500) NULL,
        Category NVARCHAR(50) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table Permissions created';
END
GO

-- RolePermissions Junction Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RolePermissions')
BEGIN
    CREATE TABLE RolePermissions (
        RolePermissionID INT IDENTITY(1,1) PRIMARY KEY,
        RoleID INT NOT NULL,
        PermissionID INT NOT NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_RolePermissions_Roles FOREIGN KEY (RoleID) REFERENCES UserRoles(RoleID),
        CONSTRAINT FK_RolePermissions_Permissions FOREIGN KEY (PermissionID) REFERENCES Permissions(PermissionID),
        CONSTRAINT UQ_RolePermissions UNIQUE(RoleID, PermissionID)
    );
    PRINT 'Table RolePermissions created';
END
GO

-- =============================================
-- 3. ASSET CATEGORIES & CONFIGURATION
-- =============================================

-- MainCategories Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'MainCategories')
BEGIN
    CREATE TABLE MainCategories (
        MainCategoryID INT IDENTITY(1,1) PRIMARY KEY,
        CategoryName NVARCHAR(100) NOT NULL UNIQUE,
        CategoryCode NVARCHAR(10) NOT NULL UNIQUE,
        Description NVARCHAR(500) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table MainCategories created';
END
GO

-- Categories Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Categories')
BEGIN
    CREATE TABLE Categories (
        CategoryID INT IDENTITY(1,1) PRIMARY KEY,
        CategoryName NVARCHAR(100) NOT NULL,
        MainCategoryID INT NOT NULL,
        Description NVARCHAR(500) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Categories_MainCategories FOREIGN KEY (MainCategoryID) REFERENCES MainCategories(MainCategoryID)
    );
    PRINT 'Table Categories created';
END
GO

-- AssetStatuses Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AssetStatuses')
BEGIN
    CREATE TABLE AssetStatuses (
        StatusID INT IDENTITY(1,1) PRIMARY KEY,
        StatusName NVARCHAR(50) NOT NULL UNIQUE,
        StatusCode NVARCHAR(20) NOT NULL UNIQUE,
        Description NVARCHAR(200) NULL,
        ColorCode NVARCHAR(20) DEFAULT 'secondary',
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table AssetStatuses created';
END
GO

-- =============================================
-- 4. ASSET MANAGEMENT
-- =============================================

-- AssetSequences Table (for ID generation)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AssetSequences')
BEGIN
    CREATE TABLE AssetSequences (
        SequenceID INT IDENTITY(1,1) PRIMARY KEY,
        CountryID INT NOT NULL,
        CompanyID INT NOT NULL,
        SequenceYear INT NOT NULL,
        Year INT NOT NULL,
        LastSequence INT DEFAULT 0,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_AssetSequences_Countries FOREIGN KEY (CountryID) REFERENCES Countries(CountryID),
        CONSTRAINT FK_AssetSequences_Companies FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
        CONSTRAINT UQ_AssetSequences UNIQUE(CountryID, CompanyID, SequenceYear)
    );
    PRINT 'Table AssetSequences created';
END
GO

-- Assets Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Assets')
BEGIN
    CREATE TABLE Assets (
        AssetID NVARCHAR(50) PRIMARY KEY,
        Picture NVARCHAR(MAX) NULL,
        MainCategory NVARCHAR(100) NOT NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Available',
        Category NVARCHAR(100) NULL,
        ModelName NVARCHAR(200) NULL,
        Brand NVARCHAR(100) NULL,
        Model NVARCHAR(200) NULL,
        CPU NVARCHAR(100) NULL,
        Ram NVARCHAR(50) NULL,
        HDD NVARCHAR(50) NULL,
        WLANMACAddress NVARCHAR(50) NULL,
        LANMACAddress NVARCHAR(50) NULL,
        Description NVARCHAR(MAX) NULL,
        SerialNumber NVARCHAR(100) NULL,
        SNType NVARCHAR(50) NULL,
        
        -- Assignment
        AssignedTo INT NULL,
        Department NVARCHAR(100) NULL,
        DateAssigned DATETIME NULL,
        
        -- Purchase Information
        DatePurchase DATETIME NULL,
        DateFirstUse DATETIME NULL,
        EndOfLife DATETIME NULL,
        Price DECIMAL(18,2) NULL,
        PONumber NVARCHAR(50) NULL,
        Invoice NVARCHAR(MAX) NULL,
        DeliveryNote NVARCHAR(MAX) NULL,
        ReplacementCost DECIMAL(18,2) NULL,
        
        -- Warranty Information
        SupplierWarrantyType NVARCHAR(100) NULL,
        SupplierWarrantyScope NVARCHAR(100) NULL,
        SupplierWarrantyServiceMethod NVARCHAR(100) NULL,
        SupplierWarrantyStart DATETIME NULL,
        SupplierWarrantyEnd DATETIME NULL,
        AdditionalWarranty NVARCHAR(100) NULL,
        AdditionalWarrantyCompany NVARCHAR(200) NULL,
        AdditionalWarrantyType NVARCHAR(100) NULL,
        AdditionalWarrantyScope NVARCHAR(100) NULL,
        AdditionalWarrantyServiceMethod NVARCHAR(100) NULL,
        AdditionalWarrantyStart DATETIME NULL,
        AdditionalWarrantyEnd DATETIME NULL,
        
        -- Location Information
        LocationID INT NULL,
        LocationName NVARCHAR(100) NULL,
        CurrentLocationID INT NULL,
        CurrentLocationName NVARCHAR(100) NULL,
        CompanyID INT NULL,
        ProvinceID INT NULL,
        CountryID INT NULL,
        
        -- Additional Fields
        ComputerName NVARCHAR(100) NULL,
        Accessories NVARCHAR(500) NULL,
        Comment NVARCHAR(MAX) NULL,
        Condition NVARCHAR(50) NULL,
        Year INT NULL,
        Month INT NULL,
        TestNumber NVARCHAR(50) NULL,
        QRCode NVARCHAR(MAX) NULL,
        
        -- Audit Fields
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CreatedBy INT NULL,
        ModifiedBy INT NULL,
        
        CONSTRAINT FK_Assets_AssignedTo FOREIGN KEY (AssignedTo) REFERENCES Users(UserID),
        CONSTRAINT FK_Assets_Location FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
        CONSTRAINT FK_Assets_CurrentLocation FOREIGN KEY (CurrentLocationID) REFERENCES Locations(LocationID),
        CONSTRAINT FK_Assets_Company FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
        CONSTRAINT FK_Assets_Province FOREIGN KEY (ProvinceID) REFERENCES Provinces(ProvinceID),
        CONSTRAINT FK_Assets_Country FOREIGN KEY (CountryID) REFERENCES Countries(CountryID),
        CONSTRAINT FK_Assets_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
        CONSTRAINT FK_Assets_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table Assets created';
END
GO

-- AssetAssignments Table (History)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AssetAssignments')
BEGIN
    CREATE TABLE AssetAssignments (
        AssignmentID INT IDENTITY(1,1) PRIMARY KEY,
        AssetID NVARCHAR(50) NOT NULL,
        UserID INT NOT NULL,
        AssignedDate DATETIME NOT NULL,
        ReturnedDate DATETIME NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Active',
        Notes NVARCHAR(MAX) NULL,
        AssignedBy INT NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_AssetAssignments_Assets FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
        CONSTRAINT FK_AssetAssignments_Users FOREIGN KEY (UserID) REFERENCES Users(UserID),
        CONSTRAINT FK_AssetAssignments_AssignedBy FOREIGN KEY (AssignedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table AssetAssignments created';
END
GO

-- AssetAuditLog Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AssetAuditLog')
BEGIN
    CREATE TABLE AssetAuditLog (
        AuditID INT IDENTITY(1,1) PRIMARY KEY,
        AssetID NVARCHAR(50) NOT NULL,
        Action NVARCHAR(50) NOT NULL,
        OldValue NVARCHAR(MAX) NULL,
        NewValue NVARCHAR(MAX) NULL,
        ChangedBy INT NULL,
        ChangedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_AssetAuditLog_Assets FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
        CONSTRAINT FK_AssetAuditLog_Users FOREIGN KEY (ChangedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table AssetAuditLog created';
END
GO

-- AssetEvents Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AssetEvents')
BEGIN
    CREATE TABLE AssetEvents (
        EventID INT IDENTITY(1,1) PRIMARY KEY,
        AssetID NVARCHAR(50) NOT NULL,
        EventType NVARCHAR(50) NOT NULL,
        EventDate DATETIME NOT NULL,
        Description NVARCHAR(MAX) NULL,
        PerformedBy INT NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_AssetEvents_Assets FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
        CONSTRAINT FK_AssetEvents_Users FOREIGN KEY (PerformedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table AssetEvents created';
END
GO

-- =============================================
-- 5. STOCK COUNT & RECONCILIATION
-- =============================================

-- StockCountSessions Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StockCountSessions')
BEGIN
    CREATE TABLE StockCountSessions (
        SessionID INT IDENTITY(1,1) PRIMARY KEY,
        SessionName NVARCHAR(200) NOT NULL,
        LocationID INT NOT NULL,
        StartDate DATETIME NOT NULL,
        EndDate DATETIME NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Planning',
        CreatedBy INT NOT NULL,
        CompletedBy INT NULL,
        CompletedAt DATETIME NULL,
        Notes NVARCHAR(MAX) NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_StockCountSessions_Location FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
        CONSTRAINT FK_StockCountSessions_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
        CONSTRAINT FK_StockCountSessions_CompletedBy FOREIGN KEY (CompletedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table StockCountSessions created';
END
GO

-- StockCounts Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StockCounts')
BEGIN
    CREATE TABLE StockCounts (
        CountID INT IDENTITY(1,1) PRIMARY KEY,
        SessionID INT NULL,
        LocationID INT NOT NULL,
        AssetID NVARCHAR(50) NOT NULL,
        UserID INT NULL,
        CountDate DATE NOT NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Pending',
        ExpectedQuantity INT NULL,
        ActualQuantity INT NULL,
        DiscrepancyType NVARCHAR(50) NULL,
        Notes NVARCHAR(500) NULL,
        CountedAt DATETIME NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_StockCounts_Session FOREIGN KEY (SessionID) REFERENCES StockCountSessions(SessionID),
        CONSTRAINT FK_StockCounts_Location FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
        CONSTRAINT FK_StockCounts_Asset FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
        CONSTRAINT FK_StockCounts_User FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
    PRINT 'Table StockCounts created';
END
GO

-- StockCountItems Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StockCountItems')
BEGIN
    CREATE TABLE StockCountItems (
        ItemID INT IDENTITY(1,1) PRIMARY KEY,
        SessionID INT NOT NULL,
        AssetID NVARCHAR(50) NOT NULL,
        ExpectedStatus NVARCHAR(50) NULL,
        ActualStatus NVARCHAR(50) NULL,
        ExpectedLocation INT NULL,
        ActualLocation INT NULL,
        DiscrepancyType NVARCHAR(50) NULL,
        CountedBy INT NULL,
        CountedAt DATETIME NULL,
        Notes NVARCHAR(MAX) NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_StockCountItems_Session FOREIGN KEY (SessionID) REFERENCES StockCountSessions(SessionID),
        CONSTRAINT FK_StockCountItems_Asset FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
        CONSTRAINT FK_StockCountItems_CountedBy FOREIGN KEY (CountedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table StockCountItems created';
END
GO

-- Reconciliations Table (Discrepancy Resolution)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Reconciliations')
BEGIN
    CREATE TABLE Reconciliations (
        ReconciliationID INT IDENTITY(1,1) PRIMARY KEY,
        StockCountID INT NULL,
        AssetID NVARCHAR(50) NOT NULL,
        DiscrepancyType NVARCHAR(50) NOT NULL,
        Description NVARCHAR(MAX) NOT NULL,
        ReportedBy INT NOT NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Reported',
        Resolution NVARCHAR(MAX) NULL,
        ResolvedBy INT NULL,
        ResolvedDate DATETIME NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Reconciliations_StockCount FOREIGN KEY (StockCountID) REFERENCES StockCounts(CountID),
        CONSTRAINT FK_Reconciliations_Asset FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
        CONSTRAINT FK_Reconciliations_ReportedBy FOREIGN KEY (ReportedBy) REFERENCES Users(UserID),
        CONSTRAINT FK_Reconciliations_ResolvedBy FOREIGN KEY (ResolvedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table Reconciliations created';
END
GO

-- =============================================
-- 6. WORKFLOW & APPROVALS
-- =============================================

-- ApprovalLevels Configuration Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ApprovalLevels')
BEGIN
    CREATE TABLE ApprovalLevels (
        LevelID INT IDENTITY(1,1) PRIMARY KEY,
        CompanyID INT NOT NULL,
        Level INT NOT NULL,
        ApproverUserID INT NOT NULL,
        RequestType NVARCHAR(50) NOT NULL,
        MinAmount DECIMAL(18,2) NULL,
        MaxAmount DECIMAL(18,2) NULL,
        IsActive BIT DEFAULT 1,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_ApprovalLevels_Company FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
        CONSTRAINT FK_ApprovalLevels_Approver FOREIGN KEY (ApproverUserID) REFERENCES Users(UserID)
    );
    PRINT 'Table ApprovalLevels created';
END
GO

-- Approvals Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Approvals')
BEGIN
    CREATE TABLE Approvals (
        ApprovalID INT IDENTITY(1,1) PRIMARY KEY,
        RequestType NVARCHAR(50) NOT NULL,
        RequestID NVARCHAR(50) NOT NULL,
        RequesterID INT NOT NULL,
        CurrentApproverID INT NULL,
        ApprovalLevel INT NOT NULL DEFAULT 1,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Pending',
        Comments NVARCHAR(MAX) NULL,
        RequestedDate DATETIME DEFAULT GETDATE(),
        ApprovedDate DATETIME NULL,
        CONSTRAINT FK_Approvals_Requester FOREIGN KEY (RequesterID) REFERENCES Users(UserID),
        CONSTRAINT FK_Approvals_CurrentApprover FOREIGN KEY (CurrentApproverID) REFERENCES Users(UserID)
    );
    PRINT 'Table Approvals created';
END
GO

-- =============================================
-- 7. BUDGET MANAGEMENT
-- =============================================

-- BudgetPlans Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'BudgetPlans')
BEGIN
    CREATE TABLE BudgetPlans (
        BudgetID INT IDENTITY(1,1) PRIMARY KEY,
        FiscalYear INT NOT NULL,
        Department NVARCHAR(100) NULL,
        Category NVARCHAR(100) NULL,
        PlannedAmount DECIMAL(18,2) NOT NULL,
        ActualAmount DECIMAL(18,2) DEFAULT 0,
        Status NVARCHAR(50) DEFAULT 'Active',
        CreatedBy INT NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_BudgetPlans_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
    );
    PRINT 'Table BudgetPlans created';
END
GO

-- =============================================
-- 8. SYSTEM TABLES
-- =============================================

-- AuditLogs Table (System-wide)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AuditLogs')
BEGIN
    CREATE TABLE AuditLogs (
        LogID INT IDENTITY(1,1) PRIMARY KEY,
        TableName NVARCHAR(100) NOT NULL,
        RecordID NVARCHAR(50) NOT NULL,
        Action NVARCHAR(20) NOT NULL,
        UserID INT NULL,
        OldValue NVARCHAR(MAX) NULL,
        NewValue NVARCHAR(MAX) NULL,
        Timestamp DATETIME DEFAULT GETDATE(),
        IPAddress NVARCHAR(50) NULL,
        CONSTRAINT FK_AuditLogs_User FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
    PRINT 'Table AuditLogs created';
END
GO

-- Notifications Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Notifications')
BEGIN
    CREATE TABLE Notifications (
        NotificationID INT IDENTITY(1,1) PRIMARY KEY,
        UserID INT NOT NULL,
        Type NVARCHAR(50) NOT NULL,
        Title NVARCHAR(200) NOT NULL,
        Message NVARCHAR(MAX) NOT NULL,
        IsRead BIT DEFAULT 0,
        RelatedEntityType NVARCHAR(50) NULL,
        RelatedEntityID NVARCHAR(50) NULL,
        CreatedAt DATETIME DEFAULT GETDATE(),
        ReadAt DATETIME NULL,
        CONSTRAINT FK_Notifications_User FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
    PRINT 'Table Notifications created';
END
GO

PRINT 'All tables created successfully!';
GO
