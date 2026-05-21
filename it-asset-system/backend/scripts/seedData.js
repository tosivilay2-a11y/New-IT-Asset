const { getConnection, closeConnection } = require('../src/config/database');
const bcrypt = require('bcryptjs');

async function seedData() {
  try {
    console.log('Starting data seeding...\n');
    
    // Wait a bit for database to be fully ready
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const pool = await getConnection();

    // 1. Seed Countries
    console.log('1. Seeding Countries...');
    await pool.query(`
      INSERT INTO Countries (CountryName, CountryCode) 
      VALUES 
        ('Thailand', 'TH'),
        ('United States', 'US'),
        ('Singapore', 'SG')
      ON CONFLICT (CountryCode) DO NOTHING
    `);
    console.log('✓ Countries seeded\n');

    // 2. Seed Provinces
    console.log('2. Seeding Provinces...');
    await pool.query(`
      INSERT INTO Provinces (ProvinceName, ProvinceCode, CountryID)
      SELECT 'Bangkok', 'BKK', CountryID FROM Countries WHERE CountryCode = 'TH'
      UNION ALL
      SELECT 'Chiang Mai', 'CNX', CountryID FROM Countries WHERE CountryCode = 'TH'
      UNION ALL
      SELECT 'California', 'CA', CountryID FROM Countries WHERE CountryCode = 'US'
      ON CONFLICT DO NOTHING
    `);
    console.log('✓ Provinces seeded\n');

    // 3. Seed Companies
    console.log('3. Seeding Companies...');
    await pool.query(`
      INSERT INTO Companies (CompanyName, CompanyCode, Address, Phone, Email)
      VALUES 
        ('ABC Corporation', 'ABC', '123 Business St', '+66-2-123-4567', 'info@abc.com'),
        ('XYZ Limited', 'XYZ', '456 Commerce Ave', '+66-2-987-6543', 'contact@xyz.com')
      ON CONFLICT (CompanyCode) DO NOTHING
    `);
    console.log('✓ Companies seeded\n');

    // 4. Seed Departments
    console.log('4. Seeding Departments...');
    const companyResult = await pool.query(`SELECT CompanyID FROM Companies WHERE CompanyCode = 'ABC' LIMIT 1`);
    const companyId = companyResult.rows[0]?.companyid;
    
    if (companyId) {
      await pool.query(`
        INSERT INTO Departments (DepartmentName, DepartmentCode, CompanyID, Description)
        VALUES 
          ('IT', 'IT', $1, 'Information Technology'),
          ('HR', 'HR', $1, 'Human Resources'),
          ('Finance', 'FIN', $1, 'Finance and Accounting'),
          ('Operations', 'OPS', $1, 'Operations')
        ON CONFLICT DO NOTHING
      `, [companyId]);
    }
    console.log('✓ Departments seeded\n');

    // 5. Seed Locations
    console.log('5. Seeding Locations...');
    const provinceResult = await pool.query(`SELECT ProvinceID FROM Provinces WHERE ProvinceCode = 'BKK' LIMIT 1`);
    const provinceId = provinceResult.rows[0]?.provinceid;
    
    if (provinceId && companyId) {
      await pool.query(`
        INSERT INTO Locations (LocationName, LocationCode, ProvinceID, CompanyID, Address)
        VALUES 
          ('Bangkok HQ', 'HQ', $1, $2, '123 Business St, Bangkok'),
          ('Bangkok - Floor 1', 'F1', $1, $2, '123 Business St, Floor 1'),
          ('Bangkok - Floor 2', 'F2', $1, $2, '123 Business St, Floor 2')
        ON CONFLICT DO NOTHING
      `, [provinceId, companyId]);
    }
    console.log('✓ Locations seeded\n');

    // 6. Seed UserTypes
    console.log('6. Seeding UserTypes...');
    await pool.query(`
      INSERT INTO UserTypes (TypeName, TypeCode, Description, ManagerLevel, CanApprove, CanManageUsers, CanAccessReports)
      VALUES 
        ('Admin', 'ADM', 'System Administrator', 3, TRUE, TRUE, TRUE),
        ('Manager', 'MGR', 'Department Manager', 2, TRUE, FALSE, TRUE),
        ('Staff', 'STF', 'Regular Staff', 1, FALSE, FALSE, FALSE)
      ON CONFLICT DO NOTHING
    `);
    console.log('✓ UserTypes seeded\n');

    // 7. Seed UserRoles
    console.log('7. Seeding UserRoles...');
    await pool.query(`
      INSERT INTO UserRoles (RoleName, Description)
      VALUES 
        ('Admin', 'System Administrator'),
        ('Manager', 'Department Manager'),
        ('User', 'Regular User')
      ON CONFLICT (RoleName) DO NOTHING
    `);
    console.log('✓ UserRoles seeded\n');

    // 8. Seed Permissions
    console.log('8. Seeding Permissions...');
    await pool.query(`
      INSERT INTO Permissions (PermissionKey, PermissionName, Description, Category)
      VALUES 
        ('asset.view', 'View Assets', 'View asset information', 'Assets'),
        ('asset.create', 'Create Assets', 'Create new assets', 'Assets'),
        ('asset.update', 'Update Assets', 'Update asset information', 'Assets'),
        ('asset.delete', 'Delete Assets', 'Delete assets', 'Assets'),
        ('asset.assign', 'Assign Assets', 'Assign assets to users', 'Assets'),
        ('asset.transfer', 'Transfer Assets', 'Transfer assets between locations', 'Assets'),
        ('user.manage', 'Manage Users', 'Manage user accounts', 'Users'),
        ('report.view', 'View Reports', 'View system reports', 'Reports')
      ON CONFLICT (PermissionKey) DO NOTHING
    `);
    console.log('✓ Permissions seeded\n');

    // 9. Seed Role Permissions
    console.log('9. Seeding Role Permissions...');
    await pool.query(`
      INSERT INTO RolePermissions (RoleID, PermissionID)
      SELECT r.RoleID, p.PermissionID
      FROM UserRoles r
      CROSS JOIN Permissions p
      WHERE r.RoleName = 'Admin'
      ON CONFLICT DO NOTHING
    `);
    
    await pool.query(`
      INSERT INTO RolePermissions (RoleID, PermissionID)
      SELECT r.RoleID, p.PermissionID
      FROM UserRoles r
      CROSS JOIN Permissions p
      WHERE r.RoleName = 'Manager' AND p.PermissionKey != 'user.manage'
      ON CONFLICT DO NOTHING
    `);
    
    await pool.query(`
      INSERT INTO RolePermissions (RoleID, PermissionID)
      SELECT r.RoleID, p.PermissionID
      FROM UserRoles r
      CROSS JOIN Permissions p
      WHERE r.RoleName = 'User' AND p.PermissionKey = 'asset.view'
      ON CONFLICT DO NOTHING
    `);
    console.log('✓ Role Permissions seeded\n');

    // 10. Seed Users
    console.log('10. Seeding Users...');
    const adminPassword = await bcrypt.hash('admin123', 10);
    const managerPassword = await bcrypt.hash('manager123', 10);
    const userPassword = await bcrypt.hash('user123', 10);

    const adminRoleResult = await pool.query(`SELECT RoleID FROM UserRoles WHERE RoleName = 'Admin' LIMIT 1`);
    const managerRoleResult = await pool.query(`SELECT RoleID FROM UserRoles WHERE RoleName = 'Manager' LIMIT 1`);
    const userRoleResult = await pool.query(`SELECT RoleID FROM UserRoles WHERE RoleName = 'User' LIMIT 1`);
    
    const adminRoleId = adminRoleResult.rows[0]?.roleid;
    const managerRoleId = managerRoleResult.rows[0]?.roleid;
    const userRoleId = userRoleResult.rows[0]?.roleid;

    const adminTypeResult = await pool.query(`SELECT UserTypeID FROM UserTypes WHERE TypeCode = 'ADM' LIMIT 1`);
    const managerTypeResult = await pool.query(`SELECT UserTypeID FROM UserTypes WHERE TypeCode = 'MGR' LIMIT 1`);
    const staffTypeResult = await pool.query(`SELECT UserTypeID FROM UserTypes WHERE TypeCode = 'STF' LIMIT 1`);
    
    const adminTypeId = adminTypeResult.rows[0]?.usertypeid;
    const managerTypeId = managerTypeResult.rows[0]?.usertypeid;
    const staffTypeId = staffTypeResult.rows[0]?.usertypeid;

    await pool.query(`
      INSERT INTO Users (EmployeeID, Username, Email, Password, FirstName, LastName, Department, Position, UserType, UserTypeID, RoleID, CompanyID, CountryID)
      VALUES 
        ('EMP001', 'admin', 'admin@example.com', $1, 'System', 'Administrator', 'IT', 'System Admin', 'Admin', $4, $7, $10, (SELECT CountryID FROM Countries WHERE CountryCode = 'TH' LIMIT 1)),
        ('EMP002', 'manager', 'manager@example.com', $2, 'IT', 'Manager', 'IT', 'IT Manager', 'Manager', $5, $8, $10, (SELECT CountryID FROM Countries WHERE CountryCode = 'TH' LIMIT 1)),
        ('EMP003', 'user', 'user@example.com', $3, 'Regular', 'User', 'HR', 'Staff', 'Staff', $6, $9, $10, (SELECT CountryID FROM Countries WHERE CountryCode = 'TH' LIMIT 1))
      ON CONFLICT (Username) DO NOTHING
    `, [adminPassword, managerPassword, userPassword, adminTypeId, managerTypeId, staffTypeId, adminRoleId, managerRoleId, userRoleId, companyId]);
    console.log('✓ Users seeded\n');

    // 11. Seed Main Categories
    console.log('11. Seeding Main Categories...');
    await pool.query(`
      INSERT INTO MainCategories (CategoryName, CategoryCode, Description)
      VALUES 
        ('Computer', 'COMP', 'Desktop and Laptop Computers'),
        ('Printer', 'PRNT', 'Printers and Scanners'),
        ('Network Equipment', 'NETW', 'Routers, Switches, Access Points'),
        ('Furniture', 'FURN', 'Office Furniture')
      ON CONFLICT (CategoryCode) DO NOTHING
    `);
    console.log('✓ Main Categories seeded\n');

    // 12. Seed Categories
    console.log('12. Seeding Categories...');
    await pool.query(`
      INSERT INTO Categories (CategoryName, MainCategoryID, Description)
      SELECT 'Desktop', MainCategoryID, 'Desktop Computers' FROM MainCategories WHERE CategoryCode = 'COMP'
      UNION ALL
      SELECT 'Laptop', MainCategoryID, 'Laptop Computers' FROM MainCategories WHERE CategoryCode = 'COMP'
      UNION ALL
      SELECT 'Laser Printer', MainCategoryID, 'Laser Printers' FROM MainCategories WHERE CategoryCode = 'PRNT'
      ON CONFLICT DO NOTHING
    `);
    console.log('✓ Categories seeded\n');

    // 13. Seed Asset Statuses
    console.log('13. Seeding Asset Statuses...');
    await pool.query(`
      INSERT INTO AssetStatuses (StatusName, StatusCode, Description, ColorCode)
      VALUES 
        ('Available', 'AVL', 'Asset is available for use', 'success'),
        ('In Use', 'USE', 'Asset is currently in use', 'primary'),
        ('Maintenance', 'MNT', 'Asset is under maintenance', 'warning'),
        ('Disposed', 'DIS', 'Asset has been disposed', 'danger')
      ON CONFLICT (StatusCode) DO NOTHING
    `);
    console.log('✓ Asset Statuses seeded\n');

    console.log('='.repeat(50));
    console.log('✓ Data seeding completed successfully!');
    console.log('='.repeat(50));
    console.log('\nDefault Users:');
    console.log('  Admin:   admin@example.com / admin123');
    console.log('  Manager: manager@example.com / manager123');
    console.log('  User:    user@example.com / user123');
    console.log('='.repeat(50));

  } catch (error) {
    console.error('✗ Seeding failed:', error.message);
    console.error(error);
    throw error;
  } finally {
    await closeConnection();
  }
}

// Run seeding
seedData()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
