"""
Check and create DeliveryAgent profile for test account
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import DeliveryAgent

try:
    user = User.objects.get(username='agent')
    print(f"✓ User found: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Name: {user.first_name} {user.last_name}")
    print(f"  User type: {user.profile.user_type}")
    
    # Check if DeliveryAgent profile exists
    try:
        delivery_profile = user.delivery_profile
        print(f"\n✓ DeliveryAgent profile exists:")
        print(f"  Name: {delivery_profile.full_name}")
        print(f"  Phone: {delivery_profile.phone}")
        print(f"  Vehicle: {delivery_profile.vehicle_type}")
    except DeliveryAgent.DoesNotExist:
        print(f"\n✗ DeliveryAgent profile NOT found!")
        print(f"\nCreating DeliveryAgent profile...")
        
        delivery_profile = DeliveryAgent.objects.create(
            user=user,
            full_name=f"{user.first_name} {user.last_name}",
            phone="9876543210",
            address="123 Delivery Street, City",
            vehicle_type="bike",
            vehicle_number="DL01AB1234",
            driving_license="DL1234567890",
            availability_status=True
        )
        
        print(f"✓ DeliveryAgent profile created successfully!")
        print(f"  Name: {delivery_profile.full_name}")
        print(f"  Phone: {delivery_profile.phone}")
        print(f"  Vehicle: {delivery_profile.vehicle_type}")
        
except User.DoesNotExist:
    print("✗ User 'agent' not found!")
    print("Please run create_test_accounts.py first")
