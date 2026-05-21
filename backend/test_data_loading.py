#!/usr/bin/env python
"""Test data loading endpoints"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import requests

def test_data_loading():
    """Test all data loading endpoints"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/health",
        "/countries/",
        "/provinces/", 
        "/companies/",
        "/main-categories/",
        "/departments/",
        "/asset-statuses/"
    ]
    
    print("=" * 60)
    print("TESTING DATA LOADING ENDPOINTS")
    print("=" * 60)
    print()
    
    all_passed = True
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/health":
                    print(f"✓ {endpoint} - Status: {data.get('status', 'unknown')}")
                else:
                    count = len(data) if isinstance(data, list) else 1
                    print(f"✓ {endpoint} - {count} records loaded")
            else:
                print(f"✗ {endpoint} - HTTP {response.status_code}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ {endpoint} - Connection error: {e}")
            all_passed = False
        except Exception as e:
            print(f"✗ {endpoint} - Error: {e}")
            all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("✓ ALL DATA LOADING TESTS PASSED!")
        print("The data loading issue has been resolved.")
    else:
        print("✗ SOME TESTS FAILED")
        print("There may still be issues with data loading.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = test_data_loading()
    sys.exit(0 if success else 1)