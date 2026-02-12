import requests

# Test register
data = {
    "username": "testuser999",
    "email": "testuser999@example.com",
    "password": "password123"
}

print("Testing Register...")
r = requests.post("http://127.0.0.1:8000/api/v1/auth/register", json=data)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
print()

# If successful or user exists, try login
if r.status_code in [200, 400]:
    print("Testing Login...")
    login_data = {
        "email": "testuser999@example.com",
        "password": "password123"
    }
    r2 = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json=login_data)
    print(f"Status: {r2.status_code}")
    print(f"Response: {r2.text}")
