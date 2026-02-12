import requests
import json

print("Testing user registration...")
url = "http://127.0.0.1:8000/api/v1/auth/register"
data = {
    "username": "testuser999",
    "email": "testuser999@example.com",
    "password": "test123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        print("✓ Registration successful!")
        result = response.json()
        print(f"✓ Access Token: {result['access_token'][:30]}...")
        print(f"✓ User: {result['user']['username']} ({result['user']['email']})")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")
