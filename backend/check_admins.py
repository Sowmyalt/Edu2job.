import os
import django
import sys

# Add the current directory to sys.path to allow imports
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # Changed to core.settings
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

admins = User.objects.filter(is_staff=True)
print(f"Found {admins.count()} admin(s):")
for admin in admins:
    print(f"ID: {admin.id}, Username: {admin.username}, Email: {admin.email}, Date Joined: {admin.date_joined}")
