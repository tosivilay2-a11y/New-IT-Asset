# 🚀 How to Run Backend

## Quick Start (Easiest)

Just double-click this file:
```
start-backend-server.bat
```

---

## Manual Method

### Step 1: Open Terminal
Open Command Prompt or PowerShell

### Step 2: Navigate to Backend
```bash
cd backend
```

### Step 3: Activate Virtual Environment
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal.

### Step 4: Start Backend
```bash
uvicorn app.main:app --reload --port 8000
```

### Step 5: Wait for Startup
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Verify It's Running

### Test 1: Health Check
Open in browser: http://localhost:8000/health

Should show:
```json
{"status":"healthy","version":"2.0.0"}
```

### Test 2: API Docs
Open in browser: http://localhost:8000/docs

Should show interactive API documentation.

### Test 3: Test Endpoint
Open in browser: http://localhost:8000/countries

Should show JSON data (or "Not Found" if routes not loaded).

---

## Stop Backend

Press `Ctrl + C` in the terminal where backend is running.

---

## Troubleshooting

### Error: "No module named 'app'"
Make sure you're in the backend directory:
```bash
cd backend
```

### Error: "venv not found"
Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Port already in use"
Kill process on port 8000:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "Database connection failed"
Make sure PostgreSQL is running.

### Error: "Table doesn't exist"
Run database setup:
```bash
recreate-database-tables.bat
```

---

## All-in-One Commands

```bash
# Navigate to backend
cd backend

# Activate venv
venv\Scripts\activate

# Start backend
uvicorn app.main:app --reload --port 8000
```

---

## Keep Backend Running

**Important:** Keep the terminal window open while backend is running.

To run in background, use:
```bash
start-backend-server.bat
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `start-backend-server.bat` | Start backend (easiest) |
| `restart-backend.bat` | Restart backend |
| `Ctrl + C` | Stop backend |
| `http://localhost:8000/health` | Health check |
| `http://localhost:8000/docs` | API docs |

---

**TL;DR:** Double-click `start-backend-server.bat` or run:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
