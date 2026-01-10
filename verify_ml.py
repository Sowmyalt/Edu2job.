import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def verify_ml_logic():
    session = requests.Session()
    
    # 1. Login
    username = "testuser_ml_v2"
    password = "password123"
    email = "test_ml_v2@example.com"
    
    # Register/Login
    session.post(f"{BASE_URL}/register/", data={"username": username, "email": email, "password": password})
    res = session.post(f"{BASE_URL}/login/", data={"username": username, "password": password})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Test Prediction for CSE Student
    print("\nTesting Prediction for CSE Student...")
    data = {
        "degree": "B.Tech",
        "specialization": "Computer Science", # Trigger "Software Developer" boost via list map
        "institution": "IIT",
        "cgpa": "8.5",
        "year": "2024",
        "certificates": ["Python", "AWS"] 
    }
    
    res = session.post(f"{BASE_URL}/predict/", json=data, headers=headers)
    
    if res.status_code == 200:
        print("PASS: Prediction API is working.")
        resp_json = res.json()
        
        if "predictions" in resp_json:
             top_match = resp_json['predictions'][0]
             print(f"Top Match: {top_match['role']}")
             print(f"Confidence: {top_match['confidence']}")
             print(f"Match Score: {top_match['match_score']}")
             print(f"Justification: {top_match['justification']}")
             
             if "Strong match" in top_match['justification']:
                 print("PASS: Boost logic applied correctly.")
             else:
                 print("FAIL: Boost logic NOT applied.")
        else:
             print("FAIL: No predictions list.")
    else:
        print(f"FAIL: {res.status_code} {res.text}")

if __name__ == "__main__":
    verify_ml_logic()
