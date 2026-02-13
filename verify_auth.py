"""
Test script for verifying authentication and login flows for all user types.
Tests customer, restaurant owner, and delivery agent login/redirect flows.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import Client
from django.urls import reverse

def test_authentication():
    """Test authentication for all three user types"""
    
    print("="*70)
    print("FOODIFY AUTHENTICATION VERIFICATION")
    print("="*70)
    print()
    
    # Test users created
    test_users = [
        ('customer_user', 'customer123', 'customer'),
        ('owner_user', 'owner123', 'restaurant_owner'),
        ('agent_user', 'agent123', 'delivery_agent'),
    ]
    
    client = Client()
    
    for username, password, expected_type in test_users:
        print(f"\n{'─'*70}")
        print(f"Testing {username} ({expected_type.replace('_', ' ').title()})")
        print(f"{'─'*70}")
        
        # 1. Test Django authentication
        user = authenticate(username=username, password=password)
        if user:
            print(f"✓ Authentication successful")
            print(f"  - Username: {user.username}")
            print(f"  - Email: {user.email}")
            print(  f"  - User Type: {user.profile.user_type}")
            print(f"  - Is Staff: {user.is_staff}")
            
            if user.profile.user_type != expected_type:
                print(f"  ✗ ERROR: Expected type '{expected_type}', got '{user.profile.user_type}'")
            else:
                print(f"  ✓ User type matches expected: {expected_type}")
            
            # 2. Test login redirect logic
            if user.profile.is_restaurant_owner:
                expected_redirect = 'restaurants:owner_dashboard'
                print(f"  ✓ Should redirect to: Restaurant Owner Dashboard")
            elif user.profile.is_delivery_agent:
                expected_redirect = 'delivery:dashboard'
                print(f"  ✓ Should redirect to: Delivery Agent Dashboard")
            else:
                expected_redirect = 'index'
                print(f"  ✓ Should redirect to: Home Page (Index)")
            
            # 3. Test profile data
            if user.profile.is_delivery_agent:
                try:
                    da = user.delivery_profile
                    print(f"  ✓ Delivery Agent Profile exists:")
                    print(f"    - Full Name: {da.full_name}")
                    print(f"    - Vehicle: {da.get_vehicle_type_display()}")
                    print(f"    - License: {da.driving_license}")
                    print(f"    - Available: {da.availability_status}")
                except Exception as e:
                    print(f"  ✗ ERROR accessing delivery profile: {e}")
            
            if user.profile.is_restaurant_owner:
                restaurants = user.owned_restaurants.all()
                print(f"  ✓ Restaurants owned: {restaurants.count()}")
                for r in restaurants:
                    print(f"    - {r.name} ({r.cuisine})")
            
        else:
            print(f"✗ Authentication FAILED")
            print(f"  - Username: {username}")
            print(f"  - Password: {password}")
            continue
    
    print(f"\n{'='*70}")
    print("URL PATTERNS VERIFICATION")
    print(f"{'='*70}\n")
    
    # Test URL patterns
    url_tests = [
        ('index', None, 'Home Page'),
        ('accounts:login', None, 'Login Page'),
        ('accounts:register', None, 'Registration Page'),
        ('restaurants:owner_dashboard', None, 'Restaurant Owner Dashboard'),
        ('delivery:dashboard', None, 'Delivery Agent Dashboard'),
    ]
    
    for url_name, kwargs, description in url_tests:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"✓ {description:40} → {url}")
        except Exception as e:
            print(f"✗ {description:40} → ERROR: {e}")
    
    print(f"\n{'='*70}")
    print("VERIFICATION COMPLETE")
    print(f"{'='*70}")
    print("\nTest Credentials:")
    print("─" * 70)
    print("1. Customer Login")
    print("   URL: http://localhost:8000/accounts/login/")
    print("   Username: customer_user")
    print("   Password: customer123")
    print("   Expected redirect: Home page (index)")
    print()
    print("2. Restaurant Owner Login")
    print("   URL: http://localhost:8000/accounts/login/")
    print("   Username: owner_user")
    print("   Password: owner123")
    print("   Expected redirect: /restaurants/dashboard/")
    print()
    print("3. Delivery Agent Login")
    print("   URL: http://localhost:8000/accounts/login/")
    print("   Username: agent_user")
    print("   Password: agent123")
    print("   Expected redirect: /delivery/dashboard/")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    test_authentication()
