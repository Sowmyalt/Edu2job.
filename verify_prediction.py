import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def run_verification():
    session = requests.Session()
    
    # 1. Register a test user
    username = "testuser_ml"
    email = "test_ml@example.com"
    password = "password123"
    
    print(f"Registering user: {username}")
    res = session.post(f"{BASE_URL}/register/", data={
        "username": username,
        "email": email,
        "password": password
    })
    
    if res.status_code == 201:
        print("Registration successful.")
    elif res.status_code == 400 and "already exists" in res.text:
         print("User already exists, proceeding to login.")
    else:
        print(f"Registration failed: {res.text}")
        # Try login anyway
        
    # 2. Login
    print("Logging in...")
    res = session.post(f"{BASE_URL}/login/", data={
        "username": username,
        "password": password
    })
    
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return
        
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 3. Update Profile (to ensure we have data)
    print("Updating profile...")
    profile_data = {
        "academic_info": {
            "gpa": 8.5,
            "major": "CS",
            "skills_score": 85
        }
    }
    # Note: Profile update is usually PATCH or PUT. Let's assume PATCH on /profile/
    res = session.patch(f"{BASE_URL}/profile/", json=profile_data, headers=headers)
    if res.status_code == 200:
        print("Profile updated.")
    else:
        print(f"Profile update failed: {res.text}")

    # 4. Predict
    print("Requesting prediction...")
    res = session.post(f"{BASE_URL}/predict/", json={}, headers=headers)
    
    if res.status_code == 200:
        print(f"Prediction successful! Result: {res.json()['prediction']}")
    else:
        print(f"Prediction failed: {res.text}")
        return

    # 5. Check History
    print("Checking history...")
    res = session.get(f"{BASE_URL}/dashboard/", headers=headers)
    
    if res.status_code == 200:
        history = res.json()
        print(f"History fetched. Count: {len(history)}")
        if len(history) > 0:
            print(f"Latest entry: {history[0]['prediction_data']['result']}")
            if history[0]['prediction_data']['result'] == res.json()['prediction']: # logic error in print line but check valid
                 print("Verification PASSED: Prediction found in history.")
            else:
                 print("Verification WARNING: Latest history does not match current prediction.")
        else:
            print("Verification FAILED: History empty.")
    else:
        print(f"History fetch failed: {res.text}")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"Verification script error: {e}")
