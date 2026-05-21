# Quick Fix: Mapper Initialization Error

## Problem
```
sqlalchemy.exc.InvalidRequestError: Could not determine join condition between parent/child tables on relationship User.assigned_assets
```

## Solution
The User model's `assigned_assets` relationship has been removed.

## Action
Just restart the backend:

```bash
# Stop current backend (Ctrl+C)
python start_server.py
```

## Done! ✅

The error should be gone. Backend will start successfully.

