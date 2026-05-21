#!/usr/bin/env python3
"""
Test script for set-default stock location endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def login():
    """Login and get access token"""
    print("Logging in...")
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None
    
    token = response.json().get("access_token")
    print(f"✅ Login successful, token: {token[:20]}...")
    return token

def test_set_default():
    """Test setting a stock location as default"""
    
    print("=" * 60)
    print("Testing Set Default Stock Location Endpoint")
    print("=" * 60)
    
    # Login first
    token = login()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, get all stock locations
    print("\n1. Fetching all stock locations...")
    response = requests.get(f"{BASE_URL}/stock-locations/", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch stock locations: {response.status_code}")
        print(response.text)
        return
    
    stock_locations = response.json()
    print(f"✅ Found {len(stock_locations)} stock locations:")
    for stock in stock_locations:
        default_status = "⭐ DEFAULT" if stock.get('stockdefault') else "  "
        print(f"   {default_status} ID: {stock['stockid']}, Name: {stock['stockname']}, Default: {stock.get('stockdefault')}")
    
    if len(stock_locations) < 2:
        print("\n⚠️  Need at least 2 stock locations to test set-default")
        return
    
    # Select a non-default stock location to set as default
    non_default = next((s for s in stock_locations if not s.get('stockdefault')), None)
    
    if not non_default:
        print("\n⚠️  All stock locations are already default (shouldn't happen)")
        return
    
    stock_id_to_set = non_default['stockid']
    print(f"\n2. Setting stock location ID {stock_id_to_set} ({non_default['stockname']}) as default...")
    
    response = requests.post(f"{BASE_URL}/stock-locations/set-default/{stock_id_to_set}", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to set default: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    print(f"✅ Response: {result['message']}")
    
    # Verify the change
    print("\n3. Verifying the change...")
    response = requests.get(f"{BASE_URL}/stock-locations/", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch stock locations: {response.status_code}")
        return
    
    stock_locations = response.json()
    print("✅ Updated stock locations:")
    for stock in stock_locations:
        default_status = "⭐ DEFAULT" if stock.get('stockdefault') else "  "
        print(f"   {default_status} ID: {stock['stockid']}, Name: {stock['stockname']}, Default: {stock.get('stockdefault')}")
    
    # Check if exactly one is default
    defaults = [s for s in stock_locations if s.get('stockdefault')]
    if len(defaults) == 1 and defaults[0]['stockid'] == stock_id_to_set:
        print("\n✅ SUCCESS: Set-default function works correctly!")
    else:
        print(f"\n❌ ERROR: Expected 1 default stock location with ID {stock_id_to_set}, but got:")
        for d in defaults:
            print(f"   ID: {d['stockid']}, Name: {d['stockname']}")

if __name__ == "__main__":
    try:
        test_set_default()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
