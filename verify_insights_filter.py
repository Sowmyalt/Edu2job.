import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def verify_insights_filter():
    session = requests.Session()
    
    # 1. Login/Register
    username = "testuser_filter"
    password = "password123"
    email = "test_filter@example.com"
    
    session.post(f"{BASE_URL}/register/", data={"username": username, "email": email, "password": password})
    res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Update Profile with B.Tech
    profile_data = {
        "education": [
            {
                "degree": "B.Tech", # Specific degree to test filter
                "specialization": "Computer Science",
                "institution": "Test Inst",
                "cgpa": "8.5",
                "year": "2024"
            }
        ]
    }
    
    print("Updating profile with B.Tech...")
    res = session.put(f"{BASE_URL}/profile/", json=profile_data, headers=headers)
    if res.status_code != 200:
        print(f"Profile update failed: {res.text}")
        return

    # 3. Get Insights
    print("Fetching insights...")
    res = session.get(f"{BASE_URL}/insights/", headers=headers)
    data = res.json()
    
    # 4. Verify Trends
    trends = data.get('degree_trends', [])
    if not trends:
        print("FAIL: No trends returned")
        return
        
    for item in trends:
        print(f"Received Trend for Degree: {item['degree']}")
        
    # Check if B.Tech is present
    btech_found = any("B.Tech" in t['degree'] or "Bachelor of Technology" in t['degree'] for t in trends)
    
    if btech_found:
        print("PASS: B.Tech trends found!")
    else:
        print("FAIL: B.Tech trends NOT found in response.")

if __name__ == "__main__":
    verify_insights_filter()
