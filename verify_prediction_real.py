import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"

def verify_real_prediction():
    session = requests.Session()
    
    # 1. Login
    username = "testuser_ui"
    password = "password123"
    print("Login...")
    res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Update Profile with Matching Fields
    # Dataset example: BBA, Artificial Intelligence, Private University, JNTU, 9.0-10.0, 4, 2026 -> Software Engineer
    # We will try to mimic this.
    print("\nupdating Profile with 'Real' Data...")
    profile_data = {
        "academic_info": {
            "education": [
                {
                    "degree": "BBA",
                    "specialization": "Artificial Intelligence",
                    "institution": "JNTU", 
                    "cgpa": "9.0-10.0",
                    "year": "2026"
                }
            ],
            "certificates": ["Cert1", "Cert2", "Cert3", "Cert4"], # 4 Certificates
            "gpa": "9.0-10.0" 
        }
    }
    
    res = session.patch(f"{BASE_URL}/profile/", json=profile_data, headers=headers)
    if res.status_code == 200:
        print("PASS: Profile updated.")
    else:
        print(f"FAIL: Profile update failed. {res.text}")
        return

    # 3. Test Prediction
    print("\nTesting Prediction...")
    # The view should now extract features from the profile we just saved
    res = session.post(f"{BASE_URL}/predict/", json={}, headers=headers)
    
    if res.status_code == 200:
        print(f"PASS: Prediction successful. Result: {res.json()['prediction']}")
    else:
        print(f"FAIL: Prediction failed. {res.text}")

if __name__ == "__main__":
    try:
        verify_real_prediction()
    except Exception as e:
        print(f"Error: {e}")
