#!/usr/bin/env python3
"""
Quick verification that System Config UI works with set-default
"""
import requests

BASE_URL = "http://localhost:8000"

# Login
print("1. Logging in...")
r = requests.post(f"{BASE_URL}/login", data={"username": "admin", "password": "admin123"})
if r.status_code != 200:
    print(f"❌ Login failed: {r.text}")
    exit(1)

token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✅ Login successful")

# Get stock locations
print("\n2. Fetching stock locations...")
r = requests.get(f"{BASE_URL}/stock-locations/", headers=headers)
if r.status_code != 200:
    print(f"❌ Failed: {r.text}")
    exit(1)

stocks = r.json()
print(f"✅ Found {len(stocks)} stock locations:")
for s in stocks:
    badge = "⭐ DEFAULT" if s.get('stockdefault') else "  "
    print(f"   {badge} ID: {s['stockid']}, Name: {s['stockname']}")

# Find non-default
non_default = next((s for s in stocks if not s.get('stockdefault')), None)
if not non_default:
    print("⚠️  All are default already")
    exit(0)

# Set as default
print(f"\n3. Setting '{non_default['stockname']}' as default...")
r = requests.post(f"{BASE_URL}/stock-locations/set-default/{non_default['stockid']}", headers=headers)
if r.status_code != 200:
    print(f"❌ Failed: {r.text}")
    exit(1)

print(f"✅ {r.json()['message']}")

# Verify
print("\n4. Verifying...")
r = requests.get(f"{BASE_URL}/stock-locations/", headers=headers)
stocks = r.json()
defaults = [s for s in stocks if s.get('stockdefault')]

if len(defaults) == 1 and defaults[0]['stockid'] == non_default['stockid']:
    print("✅ SUCCESS - Set default works correctly!")
    print(f"   Current default: {defaults[0]['stockname']}")
else:
    print("❌ FAILED - Incorrect default state")
    exit(1)
