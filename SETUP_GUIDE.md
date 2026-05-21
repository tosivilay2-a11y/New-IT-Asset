# Asset Management System - Setup Guide

## Quick Start Guide

### Option 1: Docker Setup (Recommended)

1. **Prerequisites**
   - Docker Desktop installed
   - Docker Compose installed

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Seed sample data**
   ```bash
   docker-compose exec backend python seed_data.py
   ```

### Option 2: Manual Setup

#### Backend Setup

1. **Install PostgreSQL**
   - Download and install PostgreSQL 13+
   - Create database: `createdb assetdb`

2. **Setup Python environment**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```
   
   Edit `.env` file with your database credentials:
   ```env
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/assetdb
   SECRET_KEY=your-secret-key-here
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Seed sample data (optional)**
   ```bash
   python seed_data.py
   ```

7. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Backend will be available at http://localhost:8000

#### Frontend Setup

1. **Install Node.js**
   - Download and install Node.js 16+ from nodejs.org

2. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   
   Frontend will be available at http://localhost:3000

## Database Configuration

### Switching to SQL Server

1. **Install SQL Server driver**
   ```bash
   pip install pyodbc
   ```

2. **Update DATABASE_URL in .env**
   ```env
   DATABASE_URL=mssql+pyodbc://username:password@localhost:1433/assetdb?driver=ODBC+Driver+17+for+SQL+Server
   ```

3. **Run migrations**
   ```bash
   alembic upgrade head
   ```

## Default Credentials

After seeding the database:

- **Admin Account**
  - Email: admin@example.com
  - Password: admin123

- **Staff Account**
  - Email: staff@example.com
  - Password: staff123

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Backend Issues

**Database connection error**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env file
- Ensure database exists: `createdb assetdb`

**Import errors**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Migration errors**
- Delete alembic/versions/*.py (except __init__.py)
- Recreate migrations: `alembic revision --autogenerate -m "initial"`
- Run migrations: `alembic upgrade head`

### Frontend Issues

**Module not found errors**
- Delete node_modules folder
- Delete package-lock.json
- Run `npm install` again

**API connection errors**
- Verify backend is running on port 8000
- Check CORS settings in backend/app/main.py
- Ensure API_URL in frontend/src/services/api.js is correct

**Port already in use**
- Change port in package.json: `"start": "PORT=3001 react-scripts start"`

## Development Tips

### Creating Database Migrations

After modifying models:
```bash
cd backend
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm run build
# Serve the build folder with a static server
```

## Project Structure

```
asset-management/
├── backend/
│   ├── app/
│   │   ├── core/          # Configuration, database, security
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── routes/        # API endpoints
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py        # FastAPI application
│   ├── alembic/           # Database migrations
│   ├── requirements.txt   # Python dependencies
│   └── seed_data.py       # Sample data script
├── frontend/
│   ├── public/            # Static files
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   └── App.js         # Main application
│   └── package.json       # Node dependencies
└── docker-compose.yml     # Docker configuration
```

## Next Steps

1. Customize the application for your needs
2. Add additional fields to models
3. Implement file upload for asset images
4. Add barcode/QR code scanning
5. Implement email notifications
6. Add reporting and analytics
7. Set up CI/CD pipeline
8. Deploy to production

## Support

For issues or questions:
- Check the API documentation at /docs
- Review the code comments
- Consult the README.md file
