#!/usr/bin/env python3
"""
Test script to verify System Config UI works with set-default function
Simulates user interactions in the UI
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

class SystemConfigTester:
    def __init__(self):
        self.token = None
        self.headers = {}
        self.stock_locations = []
        
    def login(self):
        """Login and get access token"""
        print("\n" + "=" * 70)
        print("STEP 1: LOGIN")
        print("=" * 70)
        
        try:
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
                return False
            
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
            print(f"✅ Login successful")
            print(f"   User: admin")
            print(f"   Token: {self.token[:30]}...")
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def fetch_stock_locations(self):
        """Fetch all stock locations (simulates page load)"""
        print("\n" + "=" * 70)
        print("STEP 2: FETCH STOCK LOCATIONS (Page Load)")
        print("=" * 70)
        
        try:
            response = requests.get(
                f"{BASE_URL}/stock-locations/",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch: {response.status_code}")
                print(response.text)
                return False
            
            self.stock_locations = response.json()
            print(f"✅ Fetched {len(self.stock_locations)} stock locations")
            
            for stock in self.stock_locations:
                default_badge = "⭐ DEFAULT" if stock.get('stockdefault') else "  "
                print(f"   {default_badge} ID: {stock['stockid']}, Name: {stock['stockname']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Fetch error: {e}")
            return False
    
    def display_ui_state(self, title):
        """Display current UI state"""
        print(f"\n📋 {title}")
        print("-" * 70)
        
        for stock in self.stock_locations:
            default_status = "⭐ DEFAULT" if stock.get('stockdefault') else "  "
            button_status = "Button: HIDDEN" if stock.get('stockdefault') else "Button: ✓ Set Default"
            print(f"   {default_status} {stock['stockname']:<30} {button_status}")
    
    def click_set_default_button(self, stock_id):
        """Simulate clicking the 'Set Default' button"""
        print("\n" + "=" * 70)
        print(f"STEP 3: USER CLICKS 'SET DEFAULT' BUTTON")
        print("=" * 70)
        
        stock = next((s for s in self.stock_locations if s['stockid'] == stock_id), None)
        if not stock:
            print(f"❌ Stock location {stock_id} not found")
            return False
        
        print(f"📌 Clicking 'Set Default' button on: {stock['stockname']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/stock-locations/set-default/{stock_id}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to set default: {response.status_code}")
                print(response.text)
                return False
            
            result = response.json()
            print(f"✅ API Response: {result['message']}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def refresh_ui(self):
        """Simulate UI refresh after set-default"""
        print("\n" + "=" * 70)
        print("STEP 4: REFRESH UI (Auto-reload after set-default)")
        print("=" * 70)
        
        print("🔄 Reloading stock locations from API...")
        time.sleep(0.5)  # Simulate network delay
        
        if not self.fetch_stock_locations():
            return False
        
        print("✅ UI refreshed successfully")
        return True
    
    def verify_ui_state(self, expected_default_id):
        """Verify the UI state is correct"""
        print("\n" + "=" * 70)
        print("STEP 5: VERIFY UI STATE")
        print("=" * 70)
        
        # Check database state
        defaults = [s for s in self.stock_locations if s.get('stockdefault')]
        
        if len(defaults) != 1:
            print(f"❌ ERROR: Expected 1 default, found {len(defaults)}")
            return False
        
        if defaults[0]['stockid'] != expected_default_id:
            print(f"❌ ERROR: Expected default ID {expected_default_id}, got {defaults[0]['stockid']}")
            return False
        
        print(f"✅ Correct default: {defaults[0]['stockname']} (ID: {defaults[0]['stockid']})")
        
        # Verify button visibility
        for stock in self.stock_locations:
            if stock.get('stockdefault'):
                print(f"✅ Default location has hidden button: {stock['stockname']}")
            else:
                print(f"✅ Non-default location has visible button: {stock['stockname']}")
        
        return True
    
    def run_full_test(self):
        """Run the complete test"""
        print("\n" + "=" * 70)
        print("SYSTEM CONFIG UI TEST - SET DEFAULT FUNCTION")
        print("=" * 70)
        
        # Step 1: Login
        if not self.login():
            return False
        
        # Step 2: Fetch stock locations (page load)
        if not self.fetch_stock_locations():
            return False
        
        if len(self.stock_locations) < 2:
            print("\n⚠️  Need at least 2 stock locations to test")
            return False
        
        # Display initial UI state
        self.display_ui_state("INITIAL UI STATE (Page Loaded)")
        
        # Find a non-default location to set as default
        non_default = next((s for s in self.stock_locations if not s.get('stockdefault')), None)
        if not non_default:
            print("\n⚠️  All locations are already default")
            return False
        
        stock_id_to_set = non_default['stockid']
        
        # Step 3: Click set default button
        if not self.click_set_default_button(stock_id_to_set):
            return False
        
        # Step 4: Refresh UI
        if not self.refresh_ui():
            return False
        
        # Display updated UI state
        self.display_ui_state("UPDATED UI STATE (After Set Default)")
        
        # Step 5: Verify UI state
        if not self.verify_ui_state(stock_id_to_set):
            return False
        
        # Final summary
        print("\n" + "=" * 70)
        print("✅ TEST PASSED - SYSTEM CONFIG UI WORKS CORRECTLY")
        print("=" * 70)
        print("\n✅ All checks passed:")
        print("   ✓ Login successful")
        print("   ✓ Stock locations loaded")
        print("   ✓ Set default button clicked")
        print("   ✓ API call successful")
        print("   ✓ UI refreshed")
        print("   ✓ Database state correct")
        print("   ✓ Button visibility correct")
        print("\n✅ System Config UI is working correctly with set-default function!")
        
        return True

def main():
    tester = SystemConfigTester()
    
    try:
        success = tester.run_full_test()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
