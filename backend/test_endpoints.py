"""Test all API endpoints"""
import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8000/api/v1"
token = None

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("TEST: Health Check")
    print("="*50)
    try:
        response = requests.get("http://127.0.0.1:8000/")
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_register():
    """Test user registration"""
    print("\n" + "="*50)
    print("TEST: Register User")
    print("="*50)
    data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ User registered successfully")
            print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
            return True
        elif response.status_code == 400:
            # User already exists
            print(f"⚠ User already exists (this is okay for testing)")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"✗ Status {response.status_code}")
            print(f"Response: {response.text}")
            # Try to get more details
            try:
                print(f"JSON: {response.json()}")
            except:
                pass
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_login():
    """Test user login"""
    global token
    print("\n" + "="*50)
    print("TEST: Login User")
    print("="*50)
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"✓ Login successful")
            print(f"✓ Access Token: {token[:20]}...")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_current_user():
    """Test get current user"""
    print("\n" + "="*50)
    print("TEST: Get Current User")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ User info retrieved")
            print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_create_log():
    """Test creating a task log"""
    print("\n" + "="*50)
    print("TEST: Create Task Log")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "task_text": "Completed a coding challenge",
        "effort_level": "oak"
    }
    try:
        response = requests.post(f"{BASE_URL}/logs/", json=data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Log created successfully")
            print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_logs():
    """Test getting user logs"""
    print("\n" + "="*50)
    print("TEST: Get All Logs")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/logs/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            logs = response.json()
            print(f"✓ Retrieved {len(logs)} logs")
            if logs:
                print(f"✓ First log: {json.dumps(logs[0], indent=2)}")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_today_logs():
    """Test getting today's logs"""
    print("\n" + "="*50)
    print("TEST: Get Today's Logs")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/logs/today", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            logs = response.json()
            print(f"✓ Retrieved {len(logs)} logs for today")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_streaks():
    """Test getting user streaks"""
    print("\n" + "="*50)
    print("TEST: Get User Streaks")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/streaks/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            streaks = response.json()
            print(f"✓ Retrieved streaks")
            print(f"✓ Response: {json.dumps(streaks, indent=2)}")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_share_forest():
    """Test creating a shared forest"""
    print("\n" + "="*50)
    print("TEST: Share Forest")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL}/share/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            share_token = result.get("share_token")
            print(f"✓ Forest shared successfully")
            print(f"✓ Share Token: {share_token}")
            return share_token
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_shared_forest(share_token):
    """Test viewing a shared forest"""
    print("\n" + "="*50)
    print("TEST: View Shared Forest")
    print("="*50)
    if not share_token:
        print("✗ No share token available, skipping")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/share/{share_token}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Shared forest retrieved")
            print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_export_json():
    """Test exporting data as JSON"""
    print("\n" + "="*50)
    print("TEST: Export Data (JSON)")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/export/json", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ JSON export successful")
            data = response.json()
            print(f"✓ Exported {len(data.get('logs', []))} logs")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_export_csv():
    """Test exporting data as CSV"""
    print("\n" + "="*50)
    print("TEST: Export Data (CSV)")
    print("="*50)
    if not token:
        print("✗ No token available, skipping")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/export/csv", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ CSV export successful")
            print(f"✓ CSV Preview (first 200 chars):\n{response.text[:200]}")
            return True
        else:
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_all_tests():
    """Run all endpoint tests"""
    print("\n" + "🌲"*20)
    print("FOREST DONE LOG - API ENDPOINT TESTS")
    print("🌲"*20)
    
    results = []
    
    # Test endpoints in order
    results.append(("Health Check", test_health()))
    results.append(("Register User", test_register()))
    results.append(("Login User", test_login()))
    results.append(("Get Current User", test_get_current_user()))
    results.append(("Create Task Log", test_create_log()))
    results.append(("Get All Logs", test_get_logs()))
    results.append(("Get Today's Logs", test_get_today_logs()))
    results.append(("Get Streaks", test_get_streaks()))
    
    share_token = test_share_forest()
    results.append(("Share Forest", bool(share_token)))
    
    if share_token:
        results.append(("View Shared Forest", test_get_shared_forest(share_token)))
    
    results.append(("Export JSON", test_export_json()))
    results.append(("Export CSV", test_export_csv()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*50)
    print(f"Results: {passed}/{total} tests passed")
    print("="*50)
    
    if passed == total:
        print("🎉 All tests passed! API is working perfectly!")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Check errors above.")

if __name__ == "__main__":
    run_all_tests()
