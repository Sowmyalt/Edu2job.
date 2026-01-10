import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def verify_insights():
    session = requests.Session()
    
    # Login
    username = "testuser_insights"
    password = "password123"
    email = "test_insights@example.com"
    
    session.post(f"{BASE_URL}/register/", data={"username": username, "email": email, "password": password})
    res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test Insights
    print("\nTesting Insights API...")
    res = session.get(f"{BASE_URL}/insights/", headers=headers)
    
    if res.status_code == 200:
        print("PASS: Insights API is working.")
        data = res.json()
        
        # Check Role Distribution
        if "role_distribution" in data and len(data['role_distribution']) > 0:
            print(f"PASS: Received Role Distribution (Top: {data['role_distribution'][0]['name']})")
        else:
            print("FAIL: Missing or empty role_distribution")
            
        # Check Degree Trends
        if "degree_trends" in data and len(data['degree_trends']) > 0:
             print(f"PASS: Received Degree Trends (Count: {len(data['degree_trends'])})")
        else:
             print("FAIL: Missing or empty degree_trends")

    else:
        print(f"FAIL: {res.status_code} {res.text}")

if __name__ == "__main__":
    verify_insights()
