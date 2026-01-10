import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def verify_module():
    session = requests.Session()
    
    # 1. Login (Reuse previous credentials or create new)
    username = "testuser_edu"
    password = "password123"
    email = "test_edu@example.com"
    
    # Register/Login
    res = session.post(f"{BASE_URL}/register/", data={"username": username, "email": email, "password": password})
    if res.status_code not in [201, 400]:
        print("Registration failed/Unknown error")
        return

    res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Test Invalid Education (Bad Year)
    print("\nTesting Invalid Year...")
    invalid_data = {
        "academic_info": {
            "education": [
                {
                    "degree": "B.Tech",
                    "institution": "IIT",
                    "year": "202", # Invalid
                    "specialization": "CS",
                    "cgpa": 9.0
                }
            ]
        }
    }
    res = session.patch(f"{BASE_URL}/profile/", json=invalid_data, headers=headers)
    if res.status_code == 400 and "4-digit" in res.text:
        print("PASS: Caught invalid year.")
    else:
        print(f"FAIL: Should have caught invalid year. Status: {res.status_code}, Resp: {res.text}")

    # 3. Test Invalid CGPA
    print("\nTesting Invalid CGPA...")
    invalid_data['academic_info']['education'][0]['year'] = "2023"
    invalid_data['academic_info']['education'][0]['cgpa'] = 11.0 # Invalid
    res = session.patch(f"{BASE_URL}/profile/", json=invalid_data, headers=headers)
    if res.status_code == 400 and "0 and 10" in res.text:
        print("PASS: Caught invalid CGPA.")
    else:
        print(f"FAIL: Should have caught invalid CGPA. Status: {res.status_code}, Resp: {res.text}")

    # 4. Test Valid Data
    print("\nTesting Valid Data...")
    valid_data = {
        "academic_info": {
            "education": [
                {
                    "degree": "B.Tech",
                    "institution": "IIT",
                    "year": "2023",
                    "specialization": "CS",
                    "cgpa": 9.5
                }
            ]
        }
    }
    res = session.patch(f"{BASE_URL}/profile/", json=valid_data, headers=headers)
    if res.status_code == 200:
        print("PASS: Accepted valid data.")
        # Verify it was saved
        profile = res.json()
        saved_edu = profile['academic_info']['education'][0]
        if saved_edu['specialization'] == "CS" and saved_edu['cgpa'] == 9.5:
             print("PASS: Data correctly saved.")
        else:
             print("FAIL: Saved data mismatch.")
    else:
         print(f"FAIL: Rejected valid data. {res.text}")

if __name__ == "__main__":
    try:
        verify_module()
    except Exception as e:
        print(f"Error: {e}")
