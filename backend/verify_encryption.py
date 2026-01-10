import os
import django
import json

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User, Profile
from users.serializers import ProfileSerializer

def verify_encryption():
    # 1. Get or Create User
    user, created = User.objects.get_or_create(username='encrypt_test', email='enc@test.com')
    if created:
        user.set_password('password')
        user.save()
        Profile.objects.create(user=user)
    
    profile = user.profile
    
    # 2. Prepare Data
    academic_data = {
        "education": [{
            "degree": "B.Tech",
            "institution": "IIT Bombay", 
            "year": "2024", 
            "cgpa": "9.0"
        }],
        "certificates": ["Cert1"]
    }
    
    print(f"Original Data: {json.dumps(academic_data, indent=2)}")
    
    # 3. Use Serializer to Update (Simulating View)
    serializer = ProfileSerializer(profile, data={'academic_info': academic_data}, partial=True)
    if serializer.is_valid():
        serializer.save()
        print("PASS: Serializer saved data.")
    else:
        print(f"FAIL: Serializer invalid. {serializer.errors}")
        return

    # 4. Verify Database Storage (Should be Encrypted)
    profile.refresh_from_db()
    raw_info = profile.academic_info
    print(f"\nRaw DB 'academic_info': {raw_info}")
    
    if isinstance(raw_info, dict) and 'ciphertext' in raw_info:
        print("PASS: Data is encrypted in Database.")
        print(f"Ciphertext: {raw_info['ciphertext'][:20]}...")
    else:
        print("FAIL: Data is NOT encrypted in Database.")
        return

    # 5. Verify Retrieval (Should be Decrypted)
    # Re-instantiate serializer with instance
    read_serializer = ProfileSerializer(profile)
    output_data = read_serializer.data['academic_info']
    print(f"\nAPI Output 'academic_info': {json.dumps(output_data, indent=2)}")
    
    if output_data == academic_data:
        print("PASS: Data successfully decrypted on read.")
    else:
        print("FAIL: Decrypted data does not match original.")

if __name__ == "__main__":
    verify_encryption()
