"""
Script to populate dummy donations with Hyderabad addresses
Run with: python manage.py shell < populate_donations.py
or: python populate_donations.py
"""
import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from donations.models import Donation
from django.utils import timezone

# Hyderabad addresses with coordinates
HYDERABAD_LOCATIONS = [
    {
        'location': 'Plot 123, Hitech City, Madhapur, Hyderabad, Telangana 500081',
        'latitude': Decimal('17.4485'),
        'longitude': Decimal('78.3908'),
    },
    {
        'location': '456 Banjara Hills Road No. 12, Hyderabad, Telangana 500034',
        'latitude': Decimal('17.4239'),
        'longitude': Decimal('78.4738'),
    },
    {
        'location': '789 Jubilee Hills, Near Filmnagar, Hyderabad, Telangana 500033',
        'latitude': Decimal('17.4315'),
        'longitude': Decimal('78.4066'),
    },
    {
        'location': 'Gachibowli Main Road, DLF Cyber City, Hyderabad, Telangana 500032',
        'latitude': Decimal('17.4401'),
        'longitude': Decimal('78.3489'),
    },
    {
        'location': 'Kondapur Main Road, Near Botanical Garden, Hyderabad, Telangana 500084',
        'latitude': Decimal('17.4616'),
        'longitude': Decimal('78.3646'),
    },
    {
        'location': 'Kukatpally Housing Board Colony, KPHB, Hyderabad, Telangana 500072',
        'latitude': Decimal('17.4849'),
        'longitude': Decimal('78.3915'),
    },
    {
        'location': 'Miyapur Metro Station Road, Hyderabad, Telangana 500049',
        'latitude': Decimal('17.4967'),
        'longitude': Decimal('78.3576'),
    },
    {
        'location': 'Ameerpet Metro Station, SR Nagar, Hyderabad, Telangana 500038',
        'latitude': Decimal('17.4376'),
        'longitude': Decimal('78.4482'),
    },
    {
        'location': 'Dilsukhnagar Bus Stop, Saidabad, Hyderabad, Telangana 500036',
        'latitude': Decimal('17.3686'),
        'longitude': Decimal('78.5242'),
    },
    {
        'location': 'Secunderabad Railway Station Road, Hyderabad, Telangana 500003',
        'latitude': Decimal('17.4344'),
        'longitude': Decimal('78.5012'),
    },
]

# Food items
FOOD_ITEMS = [
    {
        'food_name': 'Hyderabadi Biryani',
        'food_type': 'non-veg',
        'category': 'cooked',
        'description': 'Fresh Hyderabadi chicken biryani with raita and salan',
        'quantity': 25,
        'unit': 'servings',
        'hours_to_expiry': 4,
    },
    {
        'food_name': 'Veg Pulao with Paneer Curry',
        'food_type': 'veg',
        'category': 'cooked',
        'description': 'Delicious vegetable pulao with paneer butter masala',
        'quantity': 30,
        'unit': 'servings',
        'hours_to_expiry': 5,
    },
    {
        'food_name': 'Samosas & Pakoras',
        'food_type': 'veg',
        'category': 'cooked',
        'description': 'Fresh crispy samosas and mixed vegetable pakoras with chutney',
        'quantity': 50,
        'unit': 'pieces',
        'hours_to_expiry': 6,
    },
    {
        'food_name': 'Idli & Dosa Batter',
        'food_type': 'veg',
        'category': 'raw',
        'description': 'Fresh fermented idli and dosa batter, ready to cook',
        'quantity': 5,
        'unit': 'kg',
        'hours_to_expiry': 48,
    },
    {
        'food_name': 'Mixed Vegetable Curry',
        'food_type': 'veg',
        'category': 'cooked',
        'description': 'North Indian style mixed vegetable sabzi',
        'quantity': 20,
        'unit': 'servings',
        'hours_to_expiry': 4,
    },
    {
        'food_name': 'Chapatis with Dal',
        'food_type': 'veg',
        'category': 'cooked',
        'description': 'Fresh wheat chapatis with yellow dal tadka',
        'quantity': 40,
        'unit': 'servings',
        'hours_to_expiry': 3,
    },
    {
        'food_name': 'Cakes & Pastries',
        'food_type': 'veg',
        'category': 'baked',
        'description': 'Assorted fresh cakes and pastries from local bakery',
        'quantity': 15,
        'unit': 'pieces',
        'hours_to_expiry': 12,
    },
    {
        'food_name': 'Rice & Chicken Curry',
        'food_type': 'non-veg',
        'category': 'cooked',
        'description': 'Steamed rice with spicy chicken curry',
        'quantity': 35,
        'unit': 'servings',
        'hours_to_expiry': 4,
    },
    {
        'food_name': 'Fresh Fruits Package',
        'food_type': 'vegan',
        'category': 'other',
        'description': 'Assorted fresh seasonal fruits - apples, bananas, oranges',
        'quantity': 10,
        'unit': 'kg',
        'hours_to_expiry': 72,
    },
    {
        'food_name': 'Packaged Snacks & Biscuits',
        'food_type': 'veg',
        'category': 'packaged',
        'description': 'Sealed packets of chips, biscuits, and namkeen',
        'quantity': 30,
        'unit': 'packets',
        'hours_to_expiry': 168,  # 7 days
    },
]

def create_dummy_donations():
    # Get or create a donor user
    donor, created = User.objects.get_or_create(
        username='donor_admin',
        defaults={
            'email': 'donor@foodify.com',
            'first_name': 'Food',
            'last_name': 'Donor'
        }
    )
    if created:
        donor.set_password('donor123')
        donor.save()
        print(f"Created donor user: {donor.username}")
    
    # Delete existing donations
    Donation.objects.all().delete()
    print("Deleted all existing donations")
    
    # Create donations
    donations_created = 0
    for i, (food, location) in enumerate(zip(FOOD_ITEMS, HYDERABAD_LOCATIONS)):
        expiry_time = timezone.now() + timedelta(hours=food['hours_to_expiry'])
        prepared_time = timezone.now() - timedelta(hours=1)
        
        donation = Donation.objects.create(
            donor=donor,
            food_name=food['food_name'],
            food_type=food['food_type'],
            category=food['category'],
            description=food['description'],
            original_quantity=food['quantity'],
            available_quantity=food['quantity'],
            quantity_unit=food['unit'],
            location=location['location'],
            latitude=location['latitude'],
            longitude=location['longitude'],
            contact_phone='+919876543210',
            contact_name='Food Donor',
            expiry_time=expiry_time,
            prepared_time=prepared_time,
            status='available',
            pickup_instructions='Please call before arriving. Ring the doorbell.',
            tags=f"{food['food_type']}, fresh, Hyderabad"
        )
        
        donations_created += 1
        print(f"Created donation {i+1}: {donation.food_name} - {food['quantity']} {food['unit']} (expires in {food['hours_to_expiry']}h)")
    
    print(f"\n✅ Successfully created {donations_created} dummy donations!")
    print(f"Total available donations: {Donation.objects.filter(status='available').count()}")

if __name__ == '__main__':
    create_dummy_donations()
