import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def run_verification():
    session = requests.Session()
    
    # 1. Register a test user
    username = "testuser_feedback"
    email = "test_feedback@example.com"
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

    # 3. Update Profile (Ensure data for prediction)
    print("Updating profile...")
    profile_data = {
        "academic_info": {
             "education": [
                {
                    "degree": "B.Tech",
                    "institution": "IIT",
                    "cgpa": 8.5,
                    "year": 2024,
                    "specialization": "CS" 
                }
            ],
            "certificates": ["AWS"]
        }
    }
    # Update profile is PUT in serializers usually, or PATCH
    res = session.patch(f"{BASE_URL}/profile/", json=profile_data, headers=headers)
    if res.status_code == 200:
        print("Profile updated.")
    else:
        print(f"Profile update failed: {res.text}")

    # 4. Predict
    print("Requesting prediction...")
    res = session.post(f"{BASE_URL}/predict/", json={}, headers=headers)
    
    if res.status_code == 200:
        data = res.json()
        print(f"Prediction successful! Result: {data.get('prediction')}")
        history_id = data.get('history_id')
        print(f"History ID: {history_id}")
        
        if not history_id:
            print("FAILED: No history_id returned in prediction.")
            return

        # 5. Submit Feedback
        print(f"Submitting feedback for ID {history_id}...")
        feedback_data = {
            "rating": 5,
            "feedback_text": "Great prediction, very accurate!"
        }
        res_feedback = session.patch(f"{BASE_URL}/predictions/{history_id}/feedback/", json=feedback_data, headers=headers)
        
        if res_feedback.status_code == 200:
            print("Feedback submitted successfully.")
            print(res_feedback.json())
        else:
             print(f"Feedback submission failed: {res_feedback.status_code} {res_feedback.text}")
             return

        # 6. Verify in History
        print("Verifying feedback in history...")
        res_hist = session.get(f"{BASE_URL}/dashboard/", headers=headers)
        if res_hist.status_code == 200:
            history = res_hist.json()
            # Find our entry
            entry = next((item for item in history if item['id'] == history_id), None)
            if entry:
                if entry.get('rating') == 5 and entry.get('feedback_text') == "Great prediction, very accurate!":
                    print("Verification PASSED: Feedback found in history.")
                else:
                    print(f"Verification FAILED: Feedback mismatch. Got: {entry}")
            else:
                 print("Verification FAILED: Entry not found in history.")
        else:
            print("Verification FAILED: Could not fetch history.")

    else:
        print(f"Prediction failed: {res.text}")
        return

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"Verification script error: {e}")
