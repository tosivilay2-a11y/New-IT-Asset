# IT Asset Management System - Setup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "IT Asset Management - Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check PostgreSQL
Write-Host "Step 1: Checking PostgreSQL..." -ForegroundColor Yellow
$pgRunning = docker ps --filter "name=postgres" --format "{{.Names}}" 2>$null
if ($pgRunning) {
    Write-Host "✓ PostgreSQL is running: $pgRunning" -ForegroundColor Green
} else {
    Write-Host "✗ PostgreSQL is not running" -ForegroundColor Red
    Write-Host "Starting PostgreSQL..." -ForegroundColor Yellow
    docker-compose up -d db
    Start-Sleep -Seconds 5
}
Write-Host ""

# Step 2: Create Database
Write-Host "Step 2: Creating database..." -ForegroundColor Yellow
docker exec asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database created" -ForegroundColor Green
} else {
    Write-Host "⚠ Database may already exist (this is OK)" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Install Dependencies
Write-Host "Step 3: Installing Node.js dependencies..." -ForegroundColor Yellow
Set-Location backend
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Create Tables
Write-Host "Step 4: Creating database tables..." -ForegroundColor Yellow
npm run db:setup
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Tables created" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create tables" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Seed Data
Write-Host "Step 5: Seeding initial data..." -ForegroundColor Yellow
npm run db:seed
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Data seeded" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to seed data" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Success
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Database: it_asset_db" -ForegroundColor Cyan
Write-Host "Tables: 30 tables created" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default Users:" -ForegroundColor Cyan
Write-Host "  Admin:   admin@example.com / admin123" -ForegroundColor White
Write-Host "  Manager: manager@example.com / manager123" -ForegroundColor White
Write-Host "  User:    user@example.com / user123" -ForegroundColor White
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor Yellow
Write-Host "  npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Server will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
