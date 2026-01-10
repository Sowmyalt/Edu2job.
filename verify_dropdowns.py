import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def verify_dropdowns():
    session = requests.Session()
    
    # 1. Login
    username = "testuser_ui"
    password = "password123"
    email = "test_ui@example.com"
    
    print("Register/Login...")
    res = session.post(f"{BASE_URL}/register/", data={"username": username, "email": email, "password": password})
    res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Test Submission with New Fields (Dropdown Values)
    print("\nTesting Submission with Dropdown Values...")
    profile_data = {
        "academic_info": {
            "education": [
                {
                    "degree": "B.Tech",
                    "specialization": "Computer Science and Engineering (CSE)",
                    "institution": "Indian Institute of Science (IISc), Bangalore", # From Karnataka
                    "cgpa": "9.0 – 10.0", # String Range
                    "year": "2024"
                }
            ],
            # Helper for ML main endpoint
            "gpa": "9.0 – 10.0", 
            "major": "Computer Science and Engineering (CSE)"
        }
    }
    
    res = session.patch(f"{BASE_URL}/profile/", json=profile_data, headers=headers)
    if res.status_code == 200:
        print("PASS: Profile updated with dropdown values.")
        print(f"Saved CGPA: {res.json()['academic_info']['education'][0]['cgpa']}")
    else:
        print(f"FAIL: Profile update failed. {res.text}")
        return

    # 3. Test Prediction with String Range
    print("\nTesting Prediction with CGPA Range...")
    # The 'predict' endpoint uses user profile data we just saved or specific payload
    # Let's send specific payload matching new structure
    predict_payload = {
        "gpa": "8.0 – 8.9",
        "major": "Information Technology (IT)",
        "skills_score": 80
    }
    res = session.post(f"{BASE_URL}/predict/", json=predict_payload, headers=headers)
    
    if res.status_code == 200:
        print(f"PASS: Prediction successful. Result: {res.json()['prediction']}")
    else:
        print(f"FAIL: Prediction failed. {res.text}")

if __name__ == "__main__":
    try:
        verify_dropdowns()
    except Exception as e:
        print(f"Error: {e}")
