import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8001"

def test_health():
    """Test health check endpoint"""
    print("\n1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ {response.json()}")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n2. Testing Registration...")
    data = {
        "username": "testuser1234",
        "email": "test1234@example.com",
        "password": "Test@123456"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"   ✓ User created: {result['user']['username']}")
        return result['access_token']
    else:
        print(f"   ✗ Error: {response.text}")
        return None

def test_login():
    """Test user login"""
    print("\n3. Testing Login...")
    data = {
        "email": "test1234@example.com",
        "password": "Test@123456"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Login successful: {result['user']['username']}")
        return result['access_token']
    else:
        print(f"   ✗ Error: {response.text}")
        return None

def test_get_user(token):
    """Test get current user"""
    print("\n4. Testing Get Current User...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        user = response.json()
        print(f"   ✓ User: {user['username']} (Level {user['current_level']}, {user['total_points']} points)")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_create_log(token):
    """Test creating a log"""
    print("\n5. Testing Create Log...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "task_text": "Completed morning workout",
        "effort_level": "sapling"
    }
    response = requests.post(f"{BASE_URL}/api/v1/logs", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"   ✓ Log created: +{result['log']['points_earned']} points")
        print(f"   ✓ Total Points: {result['new_total_points']}, Level: {result['new_level']}")
        print(f"   ✓ Streak: {result['new_streak']} days")
        return True
    else:
        print(f"   ✗ Error: {response.text}")
        return False

def test_get_logs(token):
    """Test getting all logs"""
    print("\n6. Testing Get All Logs...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/logs", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        logs = response.json()
        print(f"   ✓ Found {len(logs)} log(s)")
        if logs:
            print(f"   ✓ Latest: {logs[0]['task_text']} ({logs[0]['points_earned']} pts)")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_today_logs(token):
    """Test getting today's logs"""
    print("\n7. Testing Get Today's Logs...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/logs/today", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):
            total_points = sum(log['points_earned'] for log in result)
            print(f"   ✓ Today: {len(result)} log(s), {total_points} points")
        else:
            print(f"   ✓ Today: {result.get('total_logs', 0)} log(s), {result.get('total_points', 0)} points")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_week_logs(token):
    """Test getting week's logs"""
    print("\n8. Testing Get Week's Logs...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/logs/week", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        logs = response.json()
        print(f"   ✓ This week: {len(logs)} log(s)")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_get_streaks(token):
    """Test getting all streaks"""
    print("\n9. Testing Get Streaks...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/streaks", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        streaks = response.json()
        print(f"   ✓ Daily: {streaks['daily']['current_count']} days")
        print(f"   ✓ Weekly: {streaks['weekly']['current_count']} weeks")
        print(f"   ✓ Monthly: {streaks['monthly']['current_count']} months")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_create_share(token):
    """Test creating a share link"""
    print("\n10. Testing Create Share Link...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, make profile public
    print("   Making profile public...")
    update_data = {"is_public": True}
    update_response = requests.patch(f"{BASE_URL}/api/v1/auth/me", json=update_data, headers=headers)
    if update_response.status_code != 200:
        print(f"   ✗ Failed to update profile: {update_response.text}")
        return None
    
    data = {
        "share_type": "profile",
        "description": "Check out my forest!"
    }
    response = requests.post(f"{BASE_URL}/api/v1/share", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"   ✓ Share link created: {result['share_token']}")
        return result['share_token']
    else:
        print(f"   ✗ Error: {response.text}")
        return None

def test_view_share(share_code):
    """Test viewing a shared forest"""
    print("\n11. Testing View Shared Forest...")
    response = requests.get(f"{BASE_URL}/api/v1/share/{share_code}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Shared by: {result['username']}")
        print(f"   ✓ Level: {result['current_level']}, Views: {result['view_count']}")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_export_json(token):
    """Test exporting data as JSON"""
    print("\n12. Testing Export JSON...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/export/json", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ User: {data['user']['username']}")
        print(f"   ✓ Logs: {len(data['logs'])}")
        print(f"   ✓ Streaks: {len(data['streaks'])}")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def test_export_csv(token):
    """Test exporting data as CSV"""
    print("\n13. Testing Export CSV...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/export/csv", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        print(f"   ✓ CSV downloaded: {len(lines)} lines")
    else:
        print(f"   ✗ Error: {response.text}")
    return response.status_code == 200

def main():
    print("=" * 60)
    print("Forest Done Log - API Endpoint Testing")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed! Server may not be running.")
        return
    
    # Test registration
    token = test_register()
    if not token:
        print("\n⚠️ Registration failed, trying login...")
        token = test_login()
    
    if not token:
        print("\n❌ Authentication failed! Cannot continue tests.")
        return
    
    # Test authenticated endpoints
    test_get_user(token)
    test_create_log(token)
    test_get_logs(token)
    test_today_logs(token)
    test_week_logs(token)
    test_get_streaks(token)
    
    # Test share endpoints
    share_code = test_create_share(token)
    if share_code:
        test_view_share(share_code)
    
    # Test export endpoints
    test_export_json(token)
    test_export_csv(token)
    
    print("\n" + "=" * 60)
    print("✅ All endpoint tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
