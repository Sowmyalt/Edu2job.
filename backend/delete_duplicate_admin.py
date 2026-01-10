import os
import django
import sys

sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # Changed to core.settings
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

users = User.objects.filter(is_staff=True).order_by('date_joined')
if users.count() > 1:
    main_admin = users[0]
    duplicates = users[1:]
    for dup in duplicates:
        print(f"Deleting duplicate admin: {dup.username} (ID: {dup.id})")
        dup.delete()
    print("Cleanup complete. Remaining admin:", main_admin.username)
else:
    print("Only one admin found, no action taken.")
