#!/usr/bin/env python3
"""
Simple test for stock location set-default endpoint
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Set Default Stock Location Endpoint")
print("=" * 60)

# Step 1: Login
print("\n1. Logging in with admin user...")
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "admin@example.com",
            "password": "admin123"
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    token = response.json().get("access_token")
    print(f"✅ Login successful")
    print(f"   Token: {token[:30]}...")
    
except Exception as e:
    print(f"❌ Login error: {e}")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Get all stock locations
print("\n2. Fetching all stock locations...")
try:
    response = requests.get(f"{BASE_URL}/stock-locations/", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch stock locations: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    stock_locations = response.json()
    print(f"✅ Found {len(stock_locations)} stock locations:")
    
    for stock in stock_locations:
        default_status = "⭐ DEFAULT" if stock.get('stockdefault') else "  "
        print(f"   {default_status} ID: {stock['stockid']}, Name: {stock['stockname']}, Default: {stock.get('stockdefault')}")
    
    if len(stock_locations) < 2:
        print("\n⚠️  Need at least 2 stock locations to test set-default")
        sys.exit(0)
    
except Exception as e:
    print(f"❌ Error fetching stock locations: {e}")
    sys.exit(1)

# Step 3: Find a non-default location
non_default = next((s for s in stock_locations if not s.get('stockdefault')), None)

if not non_default:
    print("\n⚠️  All stock locations are already default")
    sys.exit(0)

stock_id_to_set = non_default['stockid']

# Step 4: Set as default
print(f"\n3. Setting stock location ID {stock_id_to_set} ({non_default['stockname']}) as default...")
try:
    response = requests.post(
        f"{BASE_URL}/stock-locations/set-default/{stock_id_to_set}",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to set default: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    result = response.json()
    print(f"✅ Response: {result['message']}")
    
except Exception as e:
    print(f"❌ Error setting default: {e}")
    sys.exit(1)

# Step 5: Verify the change
print("\n4. Verifying the change...")
try:
    response = requests.get(f"{BASE_URL}/stock-locations/", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch stock locations: {response.status_code}")
        sys.exit(1)
    
    stock_locations = response.json()
    print("✅ Updated stock locations:")
    
    for stock in stock_locations:
        default_status = "⭐ DEFAULT" if stock.get('stockdefault') else "  "
        print(f"   {default_status} ID: {stock['stockid']}, Name: {stock['stockname']}, Default: {stock.get('stockdefault')}")
    
    # Check if exactly one is default
    defaults = [s for s in stock_locations if s.get('stockdefault')]
    if len(defaults) == 1 and defaults[0]['stockid'] == stock_id_to_set:
        print("\n✅ SUCCESS: Set-default function works correctly!")
        print(f"   Stock location '{defaults[0]['stockname']}' is now the default")
    else:
        print(f"\n❌ ERROR: Expected 1 default stock location with ID {stock_id_to_set}")
        print(f"   Found {len(defaults)} defaults:")
        for d in defaults:
            print(f"   - ID: {d['stockid']}, Name: {d['stockname']}")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Error verifying: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("Test completed successfully!")
print("=" * 60)
