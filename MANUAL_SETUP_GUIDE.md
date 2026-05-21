# Manual PostgreSQL Installation Guide for Windows

## Step-by-Step Installation

### Step 1: Download PostgreSQL

1. **Go to PostgreSQL download page**:
   - Visit: https://www.postgresql.org/download/windows/
   - Click "Download the installer"
   - Or direct link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. **Choose version**:
   - Recommended: PostgreSQL 15.x or 16.x
   - Select Windows x86-64
   - Download the installer (approximately 300MB)

### Step 2: Run the Installer

1. **Launch the installer** (postgresql-15.x-windows-x64.exe)

2. **Installation Directory**:
   - Default: `C:\Program Files\PostgreSQL\15`
   - Click "Next"

3. **Select Components**:
   - ✓ PostgreSQL Server (required)
   - ✓ pgAdmin 4 (recommended - GUI tool)
   - ✓ Stack Builder (optional)
   - ✓ Command Line Tools (required)
   - Click "Next"

4. **Data Directory**:
   - Default: `C:\Program Files\PostgreSQL\15\data`
   - Click "Next"

5. **Set Password**:
   - **IMPORTANT**: Set password for `postgres` superuser
   - Example: `postgres` (for development)
   - **Write this down!** You'll need it later
   - Click "Next"

6. **Port**:
   - Default: `5432`
   - Keep default unless it's already in use
   - Click "Next"

7. **Locale**:
   - Default locale (usually "English, United States")
   - Click "Next"

8. **Review and Install**:
   - Review settings
   - Click "Next" to install
   - Wait for installation (2-5 minutes)

9. **Complete Installation**:
   - Uncheck "Stack Builder" (not needed now)
   - Click "Finish"

### Step 3: Verify Installation

1. **Check if PostgreSQL is running**:
   - Press `Win + R`
   - Type: `services.msc`
   - Press Enter
   - Look for "postgresql-x64-15" service
   - Status should be "Running"

2. **Test command line access**:
   ```cmd
   # Open Command Prompt
   psql --version
   ```
   Should show: `psql (PostgreSQL) 15.x`

### Step 4: Create Database

**Option A: Using pgAdmin (GUI)**

1. **Open pgAdmin 4**:
   - Start Menu → PostgreSQL 15 → pgAdmin 4
   - Set master password (first time only)

2. **Connect to server**:
   - Expand "Servers" in left panel
   - Click "PostgreSQL 15"
   - Enter password you set during installation

3. **Create database**:
   - Right-click "Databases"
   - Select "Create" → "Database..."
   - Database name: `assetdb`
   - Owner: `postgres`
   - Click "Save"

**Option B: Using Command Line**

```cmd
# Open Command Prompt as Administrator
cd "C:\Program Files\PostgreSQL\15\bin"

# Create database
createdb -U postgres assetdb

# Enter password when prompted
```

Or using psql:
```cmd
# Connect to PostgreSQL
psql -U postgres

# Enter password when prompted

# Create database
CREATE DATABASE assetdb;

# Verify
\l

# Exit
\q
```

### Step 5: Configure Environment Variables (Optional but Recommended)

1. **Add PostgreSQL to PATH**:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\Program Files\PostgreSQL\15\bin`
   - Click "OK" on all dialogs

2. **Test**:
   - Open NEW Command Prompt
   - Type: `psql --version`
   - Should work from any directory

### Step 6: Configure Backend Connection

1. **Navigate to backend folder**:
   ```cmd
   cd path\to\asset-management\backend
   ```

2. **Create .env file**:
   ```cmd
   copy .env.example .env
   ```

3. **Edit .env file** (use Notepad or any text editor):
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/assetdb
   SECRET_KEY=your-secret-key-change-this-in-production-use-long-random-string
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   
   Replace `YOUR_PASSWORD` with the password you set during PostgreSQL installation.

### Step 7: Setup Python Backend

1. **Install Python** (if not already installed):
   - Download from: https://www.python.org/downloads/
   - Version 3.9 or higher
   - **Important**: Check "Add Python to PATH" during installation

2. **Create virtual environment**:
   ```cmd
   cd backend
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```
   You should see `(venv)` in your command prompt

4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```
   This will take 2-3 minutes

5. **Initialize database**:
   ```cmd
   alembic upgrade head
   ```
   This creates all tables

6. **Seed sample data**:
   ```cmd
   python seed_data.py
   ```
   This creates default users and sample data

7. **Verify setup**:
   ```cmd
   python verify_setup.py
   ```
   Should show all checks passing

8. **Start backend server**:
   ```cmd
   uvicorn app.main:app --reload
   ```
   Backend will run on http://localhost:8000

### Step 8: Setup React Frontend

1. **Install Node.js** (if not already installed):
   - Download from: https://nodejs.org/
   - Choose LTS version (20.x)
   - Run installer with default settings

2. **Open NEW Command Prompt** (for frontend):
   ```cmd
   cd path\to\asset-management\frontend
   ```

3. **Install dependencies**:
   ```cmd
   npm install
   ```
   This will take 3-5 minutes

4. **Start frontend**:
   ```cmd
   npm start
   ```
   Frontend will open automatically at http://localhost:3000

### Step 9: Login and Test

1. **Open browser**: http://localhost:3000

2. **Login with default credentials**:
   - Email: `admin@example.com`
   - Password: `admin123`

3. **You should see the dashboard!**

## Quick Reference Commands

### PostgreSQL Commands

```cmd
# Connect to database
psql -U postgres -d assetdb

# List databases
\l

# List tables
\dt

# View users
SELECT * FROM users;

# Exit
\q
```

### Backend Commands

```cmd
# Activate virtual environment
cd backend
venv\Scripts\activate

# Start server
uvicorn app.main:app --reload

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Seed data
python seed_data.py

# Verify setup
python verify_setup.py
```

### Frontend Commands

```cmd
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Troubleshooting

### PostgreSQL won't start

1. Check Windows Services:
   - Press `Win + R`, type `services.msc`
   - Find "postgresql-x64-15"
   - Right-click → Start

2. Check port 5432 is not in use:
   ```cmd
   netstat -ano | findstr :5432
   ```

### Can't connect to database

1. **Check password in .env file**
2. **Test connection**:
   ```cmd
   psql -U postgres -d assetdb
   ```
3. **Check PostgreSQL is running** (services.msc)

### "psql is not recognized"

1. Add PostgreSQL to PATH (see Step 5)
2. Or use full path:
   ```cmd
   "C:\Program Files\PostgreSQL\15\bin\psql" -U postgres
   ```

### Python/pip not found

1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Or add manually to PATH

### Port 8000 or 3000 already in use

**Find and kill process**:
```cmd
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

## Daily Development Workflow

### Starting the application:

**Terminal 1 - Backend**:
```cmd
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:
```cmd
cd frontend
npm start
```

### Stopping the application:
- Press `Ctrl + C` in each terminal

## Database Backup

### Backup database:
```cmd
pg_dump -U postgres -d assetdb -F c -f assetdb_backup.dump
```

### Restore database:
```cmd
pg_restore -U postgres -d assetdb assetdb_backup.dump
```

## Next Steps

1. ✓ PostgreSQL installed and running
2. ✓ Database created
3. ✓ Backend configured and running
4. ✓ Frontend running
5. ✓ Can login successfully

Now you can:
- Customize the application
- Add more features
- Deploy to production
- Create backups

## Support

If you encounter issues:
1. Check TROUBLESHOOTING.md
2. Check LOGIN_CHECKLIST.md
3. Run `python verify_setup.py`
4. Check logs in terminal windows
