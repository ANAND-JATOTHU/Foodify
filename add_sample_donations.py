"""
Script to create sample food donations for testing.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from donations.models import Donation
from restaurants.models import Restaurant
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

# Get users
try:
    owner_user = User.objects.get(username='owner_user')
    customer_user = User.objects.get(username='customer_user')
except User.DoesNotExist:
    print("Error: Users not found. Please create users first!")
    exit(1)

# Get some restaurants
restaurants = list(Restaurant.objects.all()[:4])

# Sample donations data
donations_data = [
    {
        'donor': owner_user,
        'restaurant': restaurants[0] if restaurants else None,
        'food_name': 'Fresh Vegetable Biryani',
        'food_type': 'veg',
        'category': 'cooked',
        'quantity_description': '5 kg (20 plates)',
        'weight_kg': Decimal('5.0'),
        'serving_count': 20,
        'description': 'Freshly prepared vegetable biryani from today\'s lunch service. Still hot and ready for pickup. Perfect condition.',
        'address': 'Pizza Paradise, Shop 12, Linking Road, Bandra West, Mumbai - 400050',
        'latitude': Decimal('19.059984'),
        'longitude': Decimal('72.829544'),
        'phone': '9876543210',
        'pickup_instructions': 'Please come to the back entrance. Ask for the manager.',
        'prepared_time': timezone.now() - timedelta(hours=2),
        'expiry_time': timezone.now() + timedelta(hours=4),
        'available_until': timezone.now() + timedelta(hours=6),
    },
    {
        'donor': owner_user,
        'restaurant': restaurants[1] if len(restaurants) > 1 else None,
        'food_name': 'Surplus Idli & Sambhar',
        'food_type': 'veg',
        'category': 'cooked',
        'quantity_description': '50 idlis with 3 liters sambhar',
        'weight_kg': Decimal('4.5'),
        'serving_count': 15,
        'description': 'Fresh South Indian breakfast items. Idlis are soft and sambhar is hot. All vegetarian and hygienically prepared.',
        'address': 'Green Leaf Cafe, Juhu Tara Road, Juhu, Mumbai - 400049',
        'latitude': Decimal('19.098042'),
        'longitude': Decimal('72.826721'),
        'phone': '9876543211',
        'pickup_instructions': 'Come between 10 AM to 2 PM. Ring the doorbell.',
        'prepared_time': timezone.now() - timedelta(hours=1),
        'expiry_time': timezone.now() + timedelta(hours=5),
    },
    {
        'donor': customer_user,
        'food_name': 'Party Leftover Pizzas',
        'food_type': 'non-veg',
        'category': 'cooked',
        'quantity_description': '8 large pizzas (mixed veg & non-veg)',
        'weight_kg': Decimal('6.0'),
        'serving_count': 25,
        'description': 'Leftover from a birthday party. Pizzas are in excellent condition, properly stored. Mix of pepperoni, chicken, and vegetarian options.',
        'address': 'Andheri West, Near Lokhandwala Complex, Mumbai - 400053',
        'latitude': Decimal('19.135989'),
        'longitude': Decimal('72.835819'),
        'phone': '9876543212',
        'pickup_instructions': 'Flat 304, Building A. Please call before coming.',
        'prepared_time': timezone.now() - timedelta(hours=3),
        'expiry_time': timezone.now() + timedelta(hours=8),
    },
    {
        'donor': owner_user,
        'restaurant': restaurants[2] if len(restaurants) > 2 else None,
        'food_name': 'Cooked Rice & Dal',
        'food_type': 'veg',
        'category': 'cooked',
        'quantity_description': '10 kg rice + 5 kg dal',
        'weight_kg': Decimal('15.0'),
        'serving_count': 40,
        'description': 'Bulk cooked rice and dal from lunch service. Perfect for community kitchens or large groups.',
        'address': 'Spice Kingdom, Andheri East, Mumbai - 400069',
        'latitude': Decimal('19.113645'),
        'longitude': Decimal('72.868176'),
        'phone': '9876543213',
        'pickup_instructions': 'Restaurant back door. Available until 8 PM.',
        'prepared_time': timezone.now() - timedelta(hours=2),
        'expiry_time': timezone.now() + timedelta(hours=6),
    },
    {
        'donor': owner_user,
        'restaurant': restaurants[3] if len(restaurants) > 3 else None,
        'food_name': 'Fresh Noodles & Fried Rice',
        'food_type': 'veg',
        'category': 'cooked',
        'quantity_description': '8 kg mixed (noodles + rice)',
        'weight_kg': Decimal('8.0'),
        'serving_count': 30,
        'description': 'Vegetarian Hakka noodles and fried rice. Freshly prepared, surplus from catering order.',
        'address': 'Dragon Wok, Worli Sea Face, Mumbai - 400018',
        'latitude': Decimal('19.018522'),
        'longitude': Decimal('72.818199'),
        'phone': '9876543214',
        'pickup_instructions': 'Ask for kitchen staff. Bring containers.',
        'prepared_time': timezone.now() - timedelta(hours=1),
        'expiry_time': timezone.now() + timedelta(hours=4),
    },
    {
        'donor': customer_user,
        'food_name': 'Packaged Bread & Biscuits',
        'food_type': 'veg',
        'category': 'packaged',
        'quantity_description': '20 bread packets + 50 biscuit packets',
        'weight_kg': Decimal('10.0'),
        'serving_count': 50,
        'description': 'Sealed packaged items nearing expiry date but still fresh. Perfect for distribution.',
        'address': 'Malad West, Near Inorbit Mall, Mumbai - 400064',
        'latitude': Decimal('19.176536'),
        'longitude': Decimal('72.835219'),
        'phone': '9876543215',
        'pickup_instructions': 'Ground floor shop. Come during business hours 9 AM - 9 PM.',
        'expiry_time': timezone.now() + timedelta(days=2),
    },
]

print("Creating sample food donations...")
print("=" * 70)

created_count = 0
for donation_data in donations_data:
    donation, created = Donation.objects.update_or_create(
        food_name=donation_data['food_name'],
        donor=donation_data['donor'],
        defaults=donation_data
    )
    
    if created:
        created_count += 1
        print(f"✓ Created: {donation.food_name}")
    else:
        print(f"→ Updated: {donation.food_name}")
    
    print(f"  Category: {donation.get_category_display()}")
    print(f"  Servings: {donation.serving_count} people")
    print(f"  Location: {donation.address[:50]}...")
    print()

print("=" * 70)
print(f"Sample donations creation complete!")
print(f"✓ {created_count} new donations created")
print(f"✓ {Donation.objects.count()} total donations in database")
print(f"\nYou can now:")
print("  1. Browse donations at: http://127.0.0.1:8000/donations/")
print("  2. Book donations and they'll appear in Orders")
print("  3. View your donations at: /donations/my-donations/")
print("  4. View your bookings at: /donations/my-bookings/")
