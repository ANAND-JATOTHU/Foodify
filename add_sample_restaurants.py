"""
Script to add sample restaurants with images and locations for testing.
Creates restaurants across Mumbai with realistic coordinates.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from django.contrib.auth.models import User
from restaurants.models import Restaurant, MenuItem
from decimal import Decimal

# Get the owner user
try:
    owner = User.objects.get(username='owner_user')
except User.DoesNotExist:
    print("Error: owner_user not found. Please run create_dummy_users.py first!")
    exit(1)

# Sample restaurant data with Mumbai coordinates
restaurants_data = [
    {
        'name': 'Pizza Paradise',
        'cuisine': 'Italian',
        'location': 'Bandra West, Mumbai',
        'latitude': Decimal('19.059984'),
        'longitude': Decimal('72.829544'),
        'distance': Decimal('3.2'),
        'rating': Decimal('4.5'),
        'description': 'Authentic Italian pizzas with hand-tossed dough and fresh mozzarella. Try our signature Margherita and Quattro Formaggi!',
        'is_veg': False,
        'menu_items': [
            {'name': 'Margherita Pizza', 'price': Decimal('299'), 'description': 'Classic tomato sauce, mozzarella, fresh basil', 'is_veg': True},
            {'name': 'Pepperoni Pizza', 'price': Decimal('399'), 'description': 'Spicy pepperoni, mozzarella, tomato sauce', 'is_veg': False},
            {'name': 'Veggie Supreme', 'price': Decimal('349'), 'description': 'Bell peppers, onions, mushrooms, olives, corn', 'is_veg': True},
            {'name': 'Chicken BBQ Pizza', 'price': Decimal('429'), 'description': 'BBQ chicken, onions, bell peppers, cheese', 'is_veg': False},
            {'name': 'Garlic Bread', 'price': Decimal('129'), 'description': 'Crispy garlic bread with herbs', 'is_veg': True},
        ]
    },
    {
        'name': 'Spice Kingdom',
        'cuisine': 'Indian',
        'location': 'Andheri East, Mumbai',
        'latitude': Decimal('19.113645'),
        'longitude': Decimal('72.868176'),
        'distance': Decimal('5.8'),
        'rating': Decimal('4.7'),
        'description': 'Traditional North Indian cuisine with rich flavors. Specializes in butter chicken, dal makhani, and tandoori dishes.',
        'is_veg': False,
        'menu_items': [
            {'name': 'Butter Chicken', 'price': Decimal('320'), 'description': 'Creamy tomato gravy with tender chicken pieces', 'is_veg': False},
            {'name': 'Paneer Tikka Masala', 'price': Decimal('280'), 'description': 'Grilled paneer in spicy masala gravy', 'is_veg': True},
            {'name': 'Dal Makhani', 'price': Decimal('220'), 'description': 'Black lentils cooked in butter and cream', 'is_veg': True},
            {'name': 'Tandoori Roti (4 pcs)', 'price': Decimal('60'), 'description': 'Freshly baked in tandoor', 'is_veg': True},
            {'name': 'Biryani (Chicken)', 'price': Decimal('299'), 'description': 'Aromatic basmati rice with spiced chicken', 'is_veg': False},
            {'name': 'Veg Biryani', 'price': Decimal('249'), 'description': 'Fragrant rice with mixed vegetables', 'is_veg': True},
        ]
    },
    {
        'name': 'Burger Bros',
        'cuisine': 'American',
        'location': 'Powai, Mumbai',
        'latitude': Decimal('19.117943'),
        'longitude': Decimal('72.905157'),
        'distance': Decimal('7.5'),
        'rating': Decimal('4.3'),
        'description': 'Juicy gourmet burgers, crispy fries, and shakes. 100% fresh beef patties and vegetarian options available.',
        'is_veg': False,
        'menu_items': [
            {'name': 'Classic Beef Burger', 'price': Decimal('249'), 'description': 'Beef patty, lettuce, tomato, special sauce', 'is_veg': False},
            {'name': 'Veggie Delight Burger', 'price': Decimal('199'), 'description': 'Crispy veg patty with fresh veggies', 'is_veg': True},
            {'name': 'Chicken Burger', 'price': Decimal('229'), 'description': 'Grilled chicken breast, mayo, lettuce', 'is_veg': False},
            {'name': 'French Fries', 'price': Decimal('99'), 'description': 'Crispy golden fries with seasoning', 'is_veg': True},
            {'name': 'Chocolate Shake', 'price': Decimal('149'), 'description': 'Thick chocolate shake topped with cream', 'is_veg': True},
        ]
    },
    {
        'name': 'Dragon Wok',
        'cuisine': 'Chinese',
        'location': 'Worli, Mumbai',
        'latitude': Decimal('19.018522'),
        'longitude': Decimal('72.818199'),
        'distance': Decimal('4.3'),
        'rating': Decimal('4.6'),
        'description': 'Authentic Chinese cuisine with Szechuan specialties. Fresh ingredients and traditional wok cooking.',
        'is_veg': False,
        'menu_items': [
            {'name': 'Hakka Noodles (Veg)', 'price': Decimal('180'), 'description': 'Stir-fried noodles with vegetables', 'is_veg': True},
            {'name': 'Chicken Fried Rice', 'price': Decimal('220'), 'description': 'Wok-tossed rice with chicken and eggs', 'is_veg': False},
            {'name': 'Manchurian (Dry)', 'price': Decimal('240'), 'description': 'Crispy vegetable balls in spicy sauce', 'is_veg': True},
            {'name': 'Chilli Chicken', 'price': Decimal('280'), 'description': 'Spicy chicken with bell peppers', 'is_veg': False},
            {'name': 'Spring Rolls (4 pcs)', 'price': Decimal('160'), 'description': 'Crispy vegetable spring rolls', 'is_veg': True},
        ]
    },
    {
        'name': 'Green Leaf Cafe',
        'cuisine': 'Indian',
        'location': 'Juhu, Mumbai',
        'latitude': Decimal('19.098042'),
        'longitude': Decimal('72.826721'),
        'distance': Decimal('2.9'),
        'rating': Decimal('4.8'),
        'description': 'Pure vegetarian restaurant serving healthy South Indian breakfast and lunch. Famous for dosas and filter coffee.',
        'is_veg': True,
        'menu_items': [
            {'name': 'Masala Dosa', 'price': Decimal('120'), 'description': 'Crispy dosa with spiced potato filling', 'is_veg': True},
            {'name': 'Idli Sambhar (3 pcs)', 'price': Decimal('80'), 'description': 'Steamed rice cakes with lentil soup', 'is_veg': True},
            {'name': 'Vada Sambhar (2 pcs)', 'price': Decimal('90'), 'description': 'Crispy lentil donuts with sambhar', 'is_veg': True},
            {'name': 'Filter Coffee', 'price': Decimal('50'), 'description': 'South Indian style aromatic coffee', 'is_veg': True},
            {'name': 'Upma', 'price': Decimal('70'), 'description': 'Semolina porridge with vegetables', 'is_veg': True},
        ]
    },
    {
        'name': 'Sushi Central',
        'cuisine': 'Japanese',
        'location': 'Lower Parel, Mumbai',
        'latitude': Decimal('18.997674'),
        'longitude': Decimal('72.830086'),
        'distance': Decimal('6.1'),
        'rating': Decimal('4.4'),
        'description': 'Fresh sushi, sashimi, and Japanese specialties. Expert chefs and premium quality seafood.',
        'is_veg': False,
        'menu_items': [
            {'name': 'California Roll (8 pcs)', 'price': Decimal('380'), 'description': 'Crab, avocado, cucumber wrapped in rice', 'is_veg': False},
            {'name': 'Veg Sushi Roll (8 pcs)', 'price': Decimal('320'), 'description': 'Fresh vegetables wrapped in seaweed', 'is_veg': True},
            {'name': 'Salmon Sashimi (5 pcs)', 'price': Decimal('450'), 'description': 'Fresh salmon slices', 'is_veg': False},
            {'name': 'Chicken Teriyaki', 'price': Decimal('340'), 'description': 'Grilled chicken in teriyaki sauce', 'is_veg': False},
            {'name': 'Miso Soup', 'price': Decimal('120'), 'description': 'Traditional Japanese soup', 'is_veg': True},
        ]
    },
    {
        'name': 'Taco Fiesta',
        'cuisine': 'Mexican',
        'location': 'Colaba, Mumbai',
        'latitude': Decimal('18.914564'),
        'longitude': Decimal('72.823118'),
        'distance': Decimal('9.2'),
        'rating': Decimal('4.2'),
        'description': 'Vibrant Mexican flavors with tacos, burritos, and nachos. Fresh guacamole made daily!',
        'is_veg': False,
        'menu_items': [
            {'name': 'Chicken Tacos (3 pcs)', 'price': Decimal('250'), 'description': 'Soft tacos with spiced chicken', 'is_veg': False},
            {'name': 'Veggie Burrito', 'price': Decimal('220'), 'description': 'Beans, rice, veggies, cheese wrapped', 'is_veg': True},
            {'name': 'Nachos Supreme', 'price': Decimal('280'), 'description': 'Tortilla chips with cheese, salsa, jalapenos', 'is_veg': True},
            {'name': 'Quesadilla', 'price': Decimal('240'), 'description': 'Grilled tortilla with cheese and chicken', 'is_veg': False},
            {'name': 'Guacamole with Chips', 'price': Decimal('180'), 'description': 'Fresh avocado dip with tortilla chips', 'is_veg': True},
        ]
    },
]

print("Creating sample restaurants and menu items...")
print("=" * 70)

created_count = 0
for restaurant_data in restaurants_data:
    # Extract menu items data
    menu_items_data = restaurant_data.pop('menu_items')
    
    # Create or update restaurant
    restaurant, created = Restaurant.objects.update_or_create(
        name=restaurant_data['name'],
        defaults={
            **restaurant_data,
            'owner': owner,
        }
    )
    
    if created:
        created_count += 1
        print(f"✓ Created: {restaurant.name} ({restaurant.cuisine})")
    else:
        print(f"→ Updated: {restaurant.name} ({restaurant.cuisine})")
    
    # Create menu items
    for item_data in menu_items_data:
        MenuItem.objects.update_or_create(
            restaurant=restaurant,
            name=item_data['name'],
            defaults=item_data
        )
    
    print(f"  Added {len(menu_items_data)} menu items")
    print(f"  Location: {restaurant.location} ({restaurant.latitude}, {restaurant.longitude})")
    print()

print("=" * 70)
print(f"Sample data creation complete!")
print(f"✓ {created_count} new restaurants created")
print(f"✓ {Restaurant.objects.count()} total restaurants in database")
print(f"✓ {MenuItem.objects.count()} total menu items in database")
