"""
Display all user accounts with their passwords (for development/debugging only)
Run this in Django shell or as a management command
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

print("\n" + "=" * 80)
print("ALL USER ACCOUNTS IN DATABASE")
print("=" * 80)

users = User.objects.all().order_by('username')

if not users:
    print("\n⚠️  No users found in database!")
    print("\nRun: python create_test_accounts.py")
else:
    for user in users:
        print(f"\n{'─' * 80}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Name: {user.first_name} {user.last_name}")
        
        # Get profile info
        try:
            profile = user.profile
            print(f"User Type: {profile.get_user_type_display()}")
            print(f"Phone: {profile.phone or 'Not set'}")
        except:
            print(f"User Type: No profile")
        
        print(f"Staff: {user.is_staff}")
        print(f"Superuser: {user.is_superuser}")
        print(f"\n⚠️  Note: Passwords are hashed and cannot be displayed")
        print(f"    For test accounts (user/owner/agent), password is: password")

print(f"\n{'=' * 80}")
print(f"Total users: {users.count()}")
print("=" * 80)

print("\n📝 TEST ACCOUNT CREDENTIALS:")
print("-" * 80)
print("Customer:        username: user      password: password")
print("Restaurant Owner: username: owner     password: password")
print("Delivery Agent:  username: agent     password: password")
print("-" * 80)
print("\n✅ Login at: http://127.0.0.1:8000/accounts/login/")
print("✅ View credentials page: http://127.0.0.1:8000/test-credentials/")
print()
