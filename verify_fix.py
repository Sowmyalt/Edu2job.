import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def verify_fix():
    session = requests.Session()
    
    # Login (using same user as before or new one)
    username = "testuser_ml" 
    password = "password123"
    
    print("Logging in...")
    try:
        res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
        if res.status_code != 200:
            print("Login failed, trying to register new user for test...")
            username = "testuser_fix"
            email = "test_fix@example.com"
            session.post(f"{BASE_URL}/register/", data={"username": username, "email": email, "password": password})
            res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
            
        token = res.json()['access']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test Case 1: Computer Science -> Should NOT be Teacher
        print("Testing Prediction for 'Computer Science'...")
        payload = {
            "gpa": 3.8,
            "major": "Computer Science", 
            "skills_score": 90
        }
        # We can override profile data by sending body params if the view supports it (I implemented it to support overriding)
        res = session.post(f"{BASE_URL}/predict/", json=payload, headers=headers)
        print(f"Input: {payload}")
        print(f"Prediction: {res.json().get('prediction')}")
        
        if res.json().get('prediction') in ['Software Engineer', 'Data Scientist', 'Consultant']:
            print("PASS: Prediction is reasonable.")
        else:
            print(f"FAIL: Prediction is '{res.json().get('prediction')}' (Expected Tech role)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_fix()
