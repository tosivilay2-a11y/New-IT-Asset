"""
Check if all admin routes are registered
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

print("=" * 70)
print("CHECKING REGISTERED ROUTES")
print("=" * 70)
print()

# Get all routes
routes = []
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        for method in route.methods:
            if method != 'HEAD':  # Skip HEAD methods
                routes.append((method, route.path))

# Sort routes
routes.sort(key=lambda x: (x[1], x[0]))

# Filter admin routes
admin_routes = [r for r in routes if any(keyword in r[1] for keyword in [
    '/countries', '/provinces', '/companies', '/main-categories', '/asset-utils'
])]

print("ADMIN ROUTES:")
print("-" * 70)

if admin_routes:
    for method, path in admin_routes:
        print(f"  {method:<8} {path}")
    print()
    print(f"✅ Found {len(admin_routes)} admin routes")
else:
    print("❌ No admin routes found!")
    print()
    print("This means the routes are not registered in main.py")
    print("Please check:")
    print("  1. Routes are imported in main.py")
    print("  2. app.include_router() is called for each route")
    print("  3. Backend server has been restarted")

print()
print("=" * 70)
print("ALL ROUTES:")
print("-" * 70)
for method, path in routes:
    print(f"  {method:<8} {path}")

print()
print(f"Total routes: {len(routes)}")
print()
print("=" * 70)
