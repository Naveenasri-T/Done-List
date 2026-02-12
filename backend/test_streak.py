import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login first
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})

if response.status_code != 200:
    print(f"Login failed: {response.text}")
    exit(1)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test streak endpoint
print("Testing GET /api/v1/streaks/")
response = requests.get(f"{BASE_URL}/streaks/", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✓ Success!")
    print(response.json())
else:
    print(f"✗ Error: {response.text}")
