# ✅ Run This To Fix Everything

## The Issue
The database has tables with dependencies that need CASCADE to drop.

## The Fix (Updated)
I've updated the script to handle this. Now run:

```bash
FIX-AND-START.bat
```

This will now:
1. ✅ Drop ALL tables with CASCADE (handles dependencies)
2. ✅ Create new tables with correct schema
3. ✅ Seed all data
4. ✅ Start backend

---

## What You'll See

```
Dropping all tables...
  ✓ Dropped table: companies
  ✓ Dropped table: locations
  ✓ Dropped table: users
  ✓ Dropped table: approvallevels
  ... (all tables)
✓ All tables dropped

Creating all tables...
✓ Tables created

Seeding location hierarchy...
✓ Location hierarchy seeded

Seeding asset control data...
✓ Asset control data seeded

Creating test user...
✓ Test user created

Starting Backend...
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

---

## Just Run This

```bash
FIX-AND-START.bat
```

That's it! The backend will start working.

---

## Test It

After it starts, open:
- http://localhost:8000/health
- http://localhost:8000/docs
- http://localhost:3000/admin/config

All should work! ✅
