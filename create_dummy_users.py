"""
Script to create dummy user profiles for testing the Foodify application.
Creates three users:
1. customer_user (Customer)
2. owner_user (Restaurant Owner)
3. agent_user (Delivery Agent)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, DeliveryAgent
from restaurants.models import Restaurant

def create_dummy_users():
    """Create dummy users for all three user types"""
    
    # Clear existing test users if they exist
    User.objects.filter(username__in=['customer_user', 'owner_user', 'agent_user']).delete()
    
    print("Creating dummy users...")
    
    # 1. Create Customer User
    customer = User.objects.create_user(
        username='customer_user',
        email='customer@foodify.com',
        password='customer123',
        first_name='John',
        last_name='Customer'
    )
    customer.profile.user_type = 'customer'
    customer.profile.phone = '9876543210'
    customer.profile.address = '123 Customer Street, Mumbai'
    customer.profile.save()
    print("✓ Created customer_user (username: customer_user, password: customer123)")
    
    # 2. Create Restaurant Owner User
    owner = User.objects.create_user(
        username='owner_user',
        email='owner@foodify.com',
        password='owner123',
        first_name='Sarah',
        last_name='Owner'
    )
    owner.profile.user_type = 'restaurant_owner'
    owner.profile.phone = '9876543211'
    owner.profile.address = '456 Restaurant Avenue, Mumbai'
    owner.profile.save()
    
    # Create a restaurant for the owner
    restaurant = Restaurant.objects.create(
        owner=owner,
        name='Sarah\'s Kitchen',
        cuisine='Italian',
        rating=4.5,
        location='Bandra, Mumbai',
        distance=2.5,
        description='Authentic Italian cuisine with a modern twist',
        is_veg=False,
        is_approved=True
    )
    print("✓ Created owner_user (username: owner_user, password: owner123)")
    print(f"  └─ Created restaurant: {restaurant.name}")
    
    # 3. Create Delivery Agent User
    agent = User.objects.create_user(
        username='agent_user',
        email='agent@foodify.com',
        password='agent123',
        first_name='Mike',
        last_name='Agent'
    )
    agent.profile.user_type = 'delivery_agent'
    agent.profile.phone = '9876543212'
    agent.profile.address = '789 Delivery Road, Mumbai'
    agent.profile.save()
    
    # Create delivery agent profile
    delivery_agent = DeliveryAgent.objects.create(
        user=agent,
        full_name='Mike Agent',
        phone='9876543212',
        address='789 Delivery Road, Mumbai',
        vehicle_type='bike',
        vehicle_number='MH-01-AB-1234',
        driving_license='DL12345678',
        availability_status=True
    )
    print("✓ Created agent_user (username: agent_user, password: agent123)")
    print(f"  └─ Created delivery agent profile: {delivery_agent.full_name}")
    
    print("\n" + "="*60)
    print("DUMMY USERS CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nYou can now login with:")
    print("1. Customer   - username: customer_user, password: customer123")
    print("2. Owner      - username: owner_user, password: owner123")
    print("3. Agent      - username: agent_user, password: agent123")
    print("="*60)

if __name__ == '__main__':
    create_dummy_users()
