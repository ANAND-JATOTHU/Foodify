import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodify_project.settings')
django.setup()

from restaurants.models import MenuItem

def add_calories_to_menu_items():
    """Add realistic calorie values to all existing menu items"""
    
    # Get all menu items
    menu_items = MenuItem.objects.all()
    
    if not menu_items:
        print("No menu items found in the database.")
        return
    
    print(f"Found {menu_items.count()} menu items. Adding calories...\n")
    
    # Calorie mapping for common food items
    calorie_map = {
        'pizza': [450, 550, 650, 750],
        'burger': [350, 450, 550, 650],
        'biryani': [400, 500, 600, 700],
        'pasta': [350, 450, 550],
        'noodles': [300, 400, 500],
        'fried rice': [350, 450, 550],
        'curry': [250, 350, 450],
        'dal': [150, 200, 250],
        'paneer': [300, 400, 500],
        'chicken': [350, 450, 550, 650],
        'mutton': [400, 500, 600],
        'fish': [250, 350, 450],
        'tandoori': [300, 400, 500],
        'korma': [400, 500, 600],
        'masala': [350, 450, 550],
        'tikka': [300, 400, 500],
        'kebab': [300, 400, 500],
        'samosa': [200, 250, 300],
        'pakora': [150, 200, 250],
        'dosa': [200, 300, 400],
        'idli': [100, 150, 200],
        'vada': [150, 200, 250],
        'paratha': [250, 350, 450],
        'naan': [200, 250, 300],
        'roti': [100, 150],
        'rice': [200, 250, 300],
        'salad': [100, 150, 200],
        'soup': [100, 150, 200],
        'sandwich': [300, 400, 500],
        'wrap': [350, 450, 550],
        'sub': [400, 500, 600],
        'taco': [200, 300, 400],
        'dumpling': [250, 350, 450],
        'spring roll': [200, 300],
        'momos': [200, 300, 400],
        'cake': [300, 400, 500],
        'ice cream': [200, 300, 400],
        'pudding': [250, 350],
        'brownie': [350, 450],
        'cookie': [100, 150, 200],
        'donut': [200, 300],
        'milkshake': [350, 450, 550],
        'smoothie': [200, 300, 400],
        'juice': [100, 150, 200],
        'coffee': [50, 100, 150],
        'tea': [50, 100],
    }
    
    updated_count = 0
    
    for item in menu_items:
        # Check if calories already set
        if item.calories:
            print(f"⏭️  {item.name}: Already has {item.calories} calories (skipping)")
            continue
        
        # Try to match with calorie map
        item_name_lower = item.name.lower()
        calories = None
        
        for food_type, cal_values in calorie_map.items():
            if food_type in item_name_lower:
                calories = random.choice(cal_values)
                break
        
        # If no match found, assign based on food type indicators
        if calories is None:
            if any(word in item_name_lower for word in ['special', 'deluxe', 'supreme', 'royal']):
                calories = random.choice([550, 650, 750, 850])
            elif any(word in item_name_lower for word in ['lite', 'light', 'healthy', 'diet']):
                calories = random.choice([150, 200, 250, 300])
            else:
                # Default calorie range
                calories = random.choice([250, 300, 350, 400, 450, 500, 550])
        
        # Update the item
        item.calories = calories
        item.save()
        updated_count += 1
        
        print(f"✅ {item.name}: {calories} calories")
    
    print(f"\n🎉 Successfully added calories to {updated_count} menu items!")
    print(f"📊 Summary:")
    print(f"   - Total items: {menu_items.count()}")
    print(f"   - Updated: {updated_count}")
    print(f"   - Already had calories: {menu_items.count() - updated_count}")

if __name__ == '__main__':
    add_calories_to_menu_items()
