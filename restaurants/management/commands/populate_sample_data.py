from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from restaurants.models import Restaurant, MenuItem
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create test users
        self.stdout.write('Creating users...')
        
        # Customer user
        if not User.objects.filter(username='customer').exists():
            customer = User.objects.create_user(
                username='customer',
                email='customer@foodify.com',
                password='password123'
            )
            customer.profile.user_type = 'customer'
            customer.profile.phone = '+91 9876543210'
            customer.profile.save()
            self.stdout.write(self.style.SUCCESS('✓ Created customer user (username: customer, password: password123)'))

        # Restaurant owner user
        if not User.objects.filter(username='owner').exists():
            owner = User.objects.create_user(
                username='owner',
                email='owner@foodify.com',
                password='password123'
            )
            owner.profile.user_type = 'restaurant_owner'
            owner.profile.phone = '+91 9876543211'
            owner.profile.save()
            self.stdout.write(self.style.SUCCESS('✓ Created restaurant owner (username: owner, password: password123)'))
        else:
            owner = User.objects.get(username='owner')

        # Create sample restaurants
        self.stdout.write('Creating restaurants...')
        
        restaurants_data = [
            {
                'name': 'Pizza Palace',
                'cuisine': 'Italian',
                'rating': Decimal('4.5'),
                'location': 'Downtown Mumbai',
                'distance': Decimal('2.5'),
                'description': 'Authentic wood-fired pizzas with fresh ingredients. Best pizzas in town!',
                'is_veg': False,
            },
            {
                'name': 'Spice Route',
                'cuisine': 'Indian',
                'rating': Decimal('4.8'),
                'location': 'Bandra West',
                'distance': Decimal('3.2'),
                'description': 'Traditional Indian cuisine with a modern twist. Famous for biryani and curries.',
                'is_veg': True,
            },
            {
                'name': 'Burger Barn',
                'cuisine': 'American',
                'rating': Decimal('4.3'),
                'location': 'Andheri East',
                'distance': Decimal('4.1'),
                'description': 'Juicy burgers and crispy fries. The ultimate burger experience!',
                'is_veg': False,
            },
            {
                'name': 'Dragon Wok',
                'cuisine': 'Chinese',
                'rating': Decimal('4.6'),
                'location': 'Powai',
                'distance': Decimal('5.0'),
                'description': 'Authentic Chinese cuisine. Best noodles and dim sum in the city!',
                'is_veg': False,
            },
        ]

        for rest_data in restaurants_data:
            restaurant, created = Restaurant.objects.get_or_create(
                name=rest_data['name'],
                owner=owner,
                defaults=rest_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created restaurant: {restaurant.name}'))
                
                # Add menu items for each restaurant
                if restaurant.name == 'Pizza Palace':
                    menu_items = [
                        {'name': 'Margherita Pizza', 'price': Decimal('299'), 'description': 'Classic tomato, mozzarella, and basil', 'is_veg': True},
                        {'name': 'Pepperoni Pizza', 'price': Decimal('399'), 'description': 'Loaded with pepperoni and cheese', 'is_veg': False},
                        {'name': 'Veggie Supreme', 'price': Decimal('349'), 'description': 'Bell peppers, olives, mushrooms, onions', 'is_veg': True},
                        {'name': 'BBQ Chicken Pizza', 'price': Decimal('449'), 'description': 'Grilled chicken with BBQ sauce', 'is_veg': False},
                    ]
                elif restaurant.name == 'Spice Route':
                    menu_items = [
                        {'name': 'Chicken Biryani', 'price': Decimal('250'), 'description': 'Aromatic basmati rice with tender chicken', 'is_veg': False},
                        {'name': 'Veg Biryani', 'price': Decimal('200'), 'description': 'Fragrant rice with mixed vegetables', 'is_veg': True},
                        {'name': 'Paneer Butter Masala', 'price': Decimal('220'), 'description': 'Cottage cheese in creamy tomato gravy', 'is_veg': True},
                        {'name': 'Dal Makhani', 'price': Decimal('180'), 'description': 'Creamy black lentils cooked overnight', 'is_veg': True},
                    ]
                elif restaurant.name == 'Burger Barn':
                    menu_items = [
                        {'name': 'Classic Beef Burger', 'price': Decimal('199'), 'description': 'Juicy beef patty with lettuce and tomato', 'is_veg': False},
                        {'name': 'Veggie Burger', 'price': Decimal('149'), 'description': 'Grilled veggie patty with special sauce', 'is_veg': True},
                        {'name': 'Chicken Burger', 'price': Decimal('179'), 'description': 'Crispy fried chicken with mayo', 'is_veg': False},
                        {'name': 'Cheese Fries', 'price': Decimal('99'), 'description': 'Golden fries loaded with cheese', 'is_veg': True},
                    ]
                else:  # Dragon Wok
                    menu_items = [
                        {'name': 'Hakka Noodles', 'price': Decimal('160'), 'description': 'Stir-fried noodles with vegetables', 'is_veg': True},
                        {'name': 'Chicken Fried Rice', 'price': Decimal('180'), 'description': 'Wok-tossed rice with chicken', 'is_veg': False},
                        {'name': 'Veg Manchurian', 'price': Decimal('150'), 'description': 'Crispy veggie balls in tangy sauce', 'is_veg': True},
                        {'name': 'Spring Rolls', 'price': Decimal('120'), 'description': 'Crispy rolls with veggie filling', 'is_veg': True},
                    ]
                
                for item_data in menu_items:
                    MenuItem.objects.get_or_create(
                        restaurant=restaurant,
                        name=item_data['name'],
                        defaults=item_data
                    )
                self.stdout.write(f'  ✓ Added {len(menu_items)} menu items')

        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created Successfully! ==='))
        self.stdout.write('\nTest Accounts:')
        self.stdout.write('  Customer: username=customer, password=password123')
        self.stdout.write('  Owner: username=owner, password=password123')
        self.stdout.write('\nYou can now browse restaurants and test all features!')
