"""
Script to add addresses to all restaurants in the database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from restaurants.models import Restaurant

# Sample addresses for different restaurant types
addresses = {
    'Pizza': '123 Pizza Street, Downtown, Hyderabad, Telangana 500001',
    'Burger': '456 Burger Avenue, Banjara Hills, Hyderabad, Telangana 500034',
    'Chinese': '789 Noodle Lane, Hitech City, Hyderabad, Telangana 500081',
    'Indian': '321 Curry Road, Jubilee Hills, Hyderabad, Telangana 500033',
    'Italian': '654 Pasta Plaza, Gachibowli, Hyderabad, Telangana 500032',
    'Mexican': '987 Taco Street, Madhapur, Hyderabad, Telangana 500081',
    'Thai': '147 Spice Avenue, Kondapur, Hyderabad, Telangana 500084',
    'Japanese': '258 Sushi Lane, Kukatpally, Hyderabad, Telangana 500072',
    'Fast Food': '369 Quick Bite Road, Ameerpet, Hyderabad, Telangana 500016',
    'Cafe': '741 Coffee Street, Begumpet, Hyderabad, Telangana 500016',
}

def add_restaurant_addresses():
    """Add addresses to restaurants that don't have them"""
    restaurants = Restaurant.objects.all()
    
    print(f"\n📍 Adding addresses to {restaurants.count()} restaurants...\n")
    
    updated_count = 0
    for restaurant in restaurants:
        # Skip if already has address
        if restaurant.location and len(restaurant.location.strip()) > 10:
            print(f"✓ {restaurant.name} already has location: {restaurant.location[:50]}...")
            continue
        
        # Determine address based on cuisine type
        address = addresses.get(restaurant.cuisine, '456 Food Street, Central Market, Hyderabad, Telangana 500001')
        
        # Update restaurant
        restaurant.location = address
        restaurant.save()
        
        updated_count += 1
        print(f"✓ Updated {restaurant.name} ({restaurant.cuisine})")
        print(f"  Location: {address}\n")
    
    print(f"\n✅ Successfully updated {updated_count} restaurant(s)!")
    print(f"📊 Total restaurants: {restaurants.count()}")

if __name__ == '__main__':
    add_restaurant_addresses()
