# Staff Management - Quick Start Guide

## What's New
Staff Management has been fully implemented in the System Configuration page. You can now:
- ✅ Add individual staff members
- ✅ View all staff in a table
- ✅ Delete staff members
- ✅ Import staff from Excel/CSV files in bulk

## Getting Started

### 1. Start the Backend
```bash
cd backend
python start_server.py
```

### 2. Create the Staff Table
Before using the feature, create the database table:
```bash
cd backend
python create_staff_table.py
```

### 3. Start the Frontend
```bash
cd frontend
npm start
```

### 4. Access Staff Management
1. Log in to the system
2. Go to **System Configuration** (⚙️)
3. Click the **👥 Staff Management** tab

## Using the Feature

### Add a Single Staff Member
1. Click **➕ Add Staff Member**
2. Fill in the form:
   - **Employee ID** (required) - e.g., EMP001
   - **Full Name** (required) - e.g., John Doe
   - **Email** (optional)
   - **Department** (optional) - e.g., IT
   - **Position** (optional) - e.g., Developer
   - **Employment Status** - Select from dropdown
3. Click **Add Staff Member**

### Import Staff from Excel
1. Click **📥 Import from Excel**
2. Click **📥 Download Template** to get the template file
3. Open the template in Excel and fill in your staff data
4. Save the file
5. Click **Choose file...** and select your file
6. Click **Import Staff**

### Delete a Staff Member
1. Find the staff member in the table
2. Click **🗑️ Delete**
3. Confirm the deletion

## Excel Template Format

Download the template and fill it like this:

| Employee ID | Full Name | Email | Department | Position | Employment Status |
|---|---|---|---|---|---|
| EMP001 | John Doe | john@example.com | IT | Developer | Active |
| EMP002 | Jane Smith | jane@example.com | HR | Manager | Active |
| EMP003 | Bob Johnson | bob@example.com | Finance | Analyst | Active |

**Required columns:**
- Employee ID
- Full Name

**Optional columns:**
- Email
- Department
- Position
- Employment Status (defaults to "Active")

## Supported File Formats
- ✅ .xlsx (Excel 2007+)
- ✅ .xls (Excel 97-2003)
- ✅ .csv (Comma-separated values)

## Features

### Validation
- Employee ID must be unique
- Email must be unique (if provided)
- Required fields: Employee ID, Full Name

### Error Handling
- Clear error messages for duplicates
- Row-by-row error reporting during import
- Success notifications after operations

### Permissions
- Only admins can add/delete/import staff
- Anyone can view the staff list

## API Endpoints (For Developers)

```
GET    /staff/              - List all staff
POST   /staff/              - Create staff member
GET    /staff/{staff_id}    - Get specific staff
DELETE /staff/{staff_id}    - Delete staff member
POST   /staff/import        - Import from file
```

## Troubleshooting

### "Staff table not found" error
Run: `python backend/create_staff_table.py`

### "Employee ID already exists"
The employee ID is already in the database. Use a different ID.

### "Email already exists"
The email is already in the database. Use a different email or leave it blank.

### Import fails with "Unsupported file format"
Make sure your file is .xlsx, .xls, or .csv format.

### Import shows "Missing Employee ID or Full Name"
Check that your Excel file has these columns and they're not empty.

## Next Steps
- View staff in asset assignments
- Generate reports with staff data
- Export staff list to Excel
- Manage staff status changes

## Support
For issues or questions, check the documentation or contact your system administrator.
