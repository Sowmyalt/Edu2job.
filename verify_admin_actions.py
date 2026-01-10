import os
import django
import requests
import json
import sys

# Add working directory to path to find 'core' module if running from backend dir
sys.path.append(os.getcwd()) 

# Setup Django standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Patch ALLOWED_HOSTS for APIClient
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users.models import PredictionHistory

User = get_user_model()

def verify_admin_actions():
    print("--- Starting Admin Actions Verification ---")
    
    # 1. Setup Users
    print("1. Setting up users...")
    admin_username = "test_admin_verifier"
    user_username = "test_user_victim"
    password = "testpassword123"
    
    # Create/Get Admin
    try:
        admin = User.objects.get(username=admin_username)
        admin.set_password(password)
        admin.save()
    except User.DoesNotExist:
        admin = User.objects.create_superuser(username=admin_username, email="admin@test.com", password=password)
    
    # Create/Get Victim User
    try:
        user_to_delete = User.objects.get(username=user_username)
        user_to_delete.delete() # Ensure fresh start
    except User.DoesNotExist:
        pass
    
    user_to_delete = User.objects.create_user(username=user_username, email="victim@test.com", password=password)
    user_id = user_to_delete.id
    print(f"Created user to delete: {user_username} (ID: {user_id})")

    # 2. Login as Admin via API (to get token if needed, or just use force_authenticate with Client)
    # Using Django Test Client for simplicity in accessing views directly if possible, 
    # but let's use requests against the running server for true E2E, OR Client for unit-integration style.
    # Given the previous script used requests, let's stick to that IF server is running. 
    # BUT relying on external server is flaky. Let's use DRF APIClient which doesn't need running server.
    
    client = APIClient()
    client.force_authenticate(user=admin)
    
    # 3. Test List Users
    print("2. Testing User List API...")
    response = client.get('/api/admin/users/')
    if response.status_code == 200:
        users = response.json()
        print(f"Success. Found {len(users)} users.")
        found = any(u['username'] == user_username for u in users)
        if found:
            print("Target user found in list.")
        else:
            print("ERROR: Target user NOT found in list.")
            return
    else:
        print(f"ERROR: Failed to list users. Status: {response.status_code}")
        return

    # 4. Test Delete User
    print(f"3. Testing Delete User API (ID: {user_id})...")
    response = client.delete(f'/api/admin/users/{user_id}/')
    if response.status_code == 204:
        print("Success. Delete request successful.")
    else:
        print(f"ERROR: Failed to delete user. Status: {response.status_code}")
        return

    # Verify Deletion
    if not User.objects.filter(id=user_id).exists():
        print("Verification: User successfully removed from DB.")
    else:
        print("ERROR: User still exists in DB!")
        return

    # 5. Test Retrain with Feedback
    print("4. Testing Retrain with Feedback API...")
    # Create some mock feedback
    PredictionHistory.objects.create(
        user=admin,
        prediction_data={'input': {'Degree': 'B.Tech', 'Specialization': 'CS', 'College_Name': 'IIT', 'CGPA': 9.0, 'Graduation_Year': 2024}, 'result': 'Wrong Role'},
        correction='Data Scientist',
        is_flagged=True
    )
    
    # Call Retrain
    response = client.post('/api/admin/retrain/', {'include_feedback': 'true'}, format='multipart')
    if response.status_code == 200:
        print(f"Success: {response.json().get('message')}")
    else:
        print(f"ERROR: Retrain failed. Status: {response.status_code} - {response.data}")

    print("--- Verification Complete ---")

if __name__ == "__main__":
    verify_admin_actions()
