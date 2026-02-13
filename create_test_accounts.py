"""
Create test accounts for all user types with simple credentials.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

# Test accounts data
accounts = [
    {
        'username': 'user',
        'password': 'password',
        'email': 'user@foodify.com',
        'first_name': 'Test',
        'last_name': 'User',
        'user_type': 'customer',
    },
    {
        'username': 'owner',
        'password': 'password',
        'email': 'owner@foodify.com',
        'first_name': 'Restaurant',
        'last_name': 'Owner',
        'user_type': 'restaurant_owner',
    },
    {
        'username': 'agent',
        'password': 'password',
        'email': 'agent@foodify.com',
        'first_name': 'Delivery',
        'last_name': 'Agent',
        'user_type': 'delivery_agent',
    },
]

print("Creating test accounts...")
print("=" * 70)

for account_data in accounts:
    username = account_data['username']
    password = account_data['password']
    user_type = account_data['user_type']
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        # Update password in case it changed
        user.set_password(password)
        user.email = account_data['email']
        user.first_name = account_data['first_name']
        user.last_name = account_data['last_name']
        user.save()
        print(f"✓ Updated existing user: {username}")
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=account_data['email'],
            first_name=account_data['first_name'],
            last_name=account_data['last_name']
        )
        print(f"✓ Created new user: {username}")
    
    # Ensure profile exists and update it
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Set user type
    profile.user_type = user_type
    
    # Set phone number
    profile.phone = f"98765432{accounts.index(account_data):02d}"
    profile.save()
    
    print(f"  → Type: {user_type}")
    print(f"  → Email: {account_data['email']}")
    print(f"  → Phone: {profile.phone}")
    print()

print("=" * 70)
print("Test accounts created successfully!")
print()
print("Login Credentials:")
print("-" * 70)
print("Customer Account:")
print("  Username: user")
print("  Password: password")
print()
print("Restaurant Owner Account:")
print("  Username: owner")
print("  Password: password")
print()
print("Delivery Agent Account:")
print("  Username: agent")
print("  Password: password")
print()
print("=" * 70)
print("IMPORTANT: If you're getting CSRF errors:")
print("1. Clear your browser cache and cookies")
print("2. Try in an incognito/private window")
print("3. Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)")
print()
print("Login at: http://127.0.0.1:8000/accounts/login/")
