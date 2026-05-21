#!/usr/bin/env python3

import requests
import json

def test_categories():
    """Test what categories are available via API"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== CHECKING AVAILABLE CATEGORIES ===")
    print("1. Logging in...")
    
    try:
        login_response = requests.post(login_url, data=login_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return
        
        token = login_response.json()['access_token']
        print("Login successful!")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Check main categories
        print("\n2. Checking main categories...")
        try:
            response = requests.get("http://localhost:8000/admin/main-categories", headers=headers)
            if response.status_code == 200:
                categories = response.json()
                print("Main Categories:")
                for cat in categories:
                    print(f"  ID: {cat.get('maincategoryid')}, Name: {cat.get('categoryname')}")
            else:
                print(f"Failed to get categories: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error getting categories: {e}")
        
        # Check countries
        print("\n3. Checking countries...")
        try:
            response = requests.get("http://localhost:8000/countries/", headers=headers)
            if response.status_code == 200:
                countries = response.json()
                print("Countries:")
                for country in countries:
                    print(f"  ID: {country.get('countryid')}, Name: {country.get('countryname')}")
            else:
                print(f"Failed to get countries: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error getting countries: {e}")
        
        # Check provinces
        print("\n4. Checking provinces...")
        try:
            response = requests.get("http://localhost:8000/provinces/", headers=headers)
            if response.status_code == 200:
                provinces = response.json()
                print("Provinces:")
                for province in provinces:
                    print(f"  ID: {province.get('provinceid')}, Name: {province.get('provincename')}")
            else:
                print(f"Failed to get provinces: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error getting provinces: {e}")
        
        # Check companies
        print("\n5. Checking companies...")
        try:
            response = requests.get("http://localhost:8000/companies/", headers=headers)
            if response.status_code == 200:
                companies = response.json()
                print("Companies:")
                for company in companies:
                    print(f"  ID: {company.get('companyid')}, Name: {company.get('companyname')}")
            else:
                print(f"Failed to get companies: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error getting companies: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_categories()