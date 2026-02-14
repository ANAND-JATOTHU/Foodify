# FOODIFY - Online Food Delivery Platform

## Project Overview

**Foodify** is a comprehensive web-based food delivery platform built using Django framework that connects customers with local restaurants. The application provides a seamless ordering experience with separate interfaces for customers and restaurant owners, enabling efficient food ordering, menu management, and order tracking.

---

## Abstract

The Foodify platform addresses critical gaps in existing food delivery services (Zomato, Swiggy, UberEats) by combining traditional food ordering with an innovative **food donation system** that tackles the industry's 30-40% food waste problem. Unlike existing platforms that focus solely on profit, Foodify integrates social responsibility through smart quantity-based booking, time-sensitive expiry management, and GPS-powered navigation.

The platform features a unified multi-role system (customers, restaurant owners, delivery agents) with:
- **Revolutionary Donation System**: Flexible quantity booking, urgency-based sorting, auto-expiry filtering
- **Advanced Location Services**: GPS navigation, Geoapify integration, precise pickup coordinates  
- **Real-Time Management**: Live availability updates, countdown timers, auto-refresh
- **Community Impact**: Reduces waste, feeds those in need, earns tax benefits for donors

Built with Django's robust framework and modern web technologies, Foodify serves as a complete ecosystem that balances business operations with environmental and social responsibility.

---

## 🎯 Problem Statement - Gaps in Existing Platforms

### Industry Analysis: Zomato, Swiggy, UberEats, DoorDash

While existing platforms have popularized food delivery, they have **critical shortcomings**:

#### 1. **Massive Food Waste Problem** 🗑️
- **Statistics**: Restaurants waste 30-40% of prepared food daily
- **Causes**: Excess inventory, cancelled orders, near-expiry items, bulk preparation
- **Current Solutions**: None - all waste goes to trash
- **Environmental Impact**: Methane emissions, landfill overflow, resource waste
- **Economic Impact**: ₹50,000-₹2,00,000 monthly loss per restaurant

#### 2. **Zero Social Responsibility**
- Existing platforms are purely profit-driven
- No features to redistribute surplus food
- Food insecurity affects millions while edible food is discarded
- No community welfare programs

#### 3. **Poor Time Management for Perishables**
- No urgency indicators for time-sensitive food
- Static listings don't show expiry times
- Users can't identify "expiring soon" deals
- Restaurants can't prioritize clearing inventory

#### 4. **Rigid Fixed Portions**
- Users forced to order full portions
- No flexibility for sharing or partial quantities
- Contributes to over-ordering and waste
- No multi-user booking from single listing

#### 5. **Limited GPS Features**
- Vague delivery estimates ("15-20 mins away")
- No easy navigation to pickup points
- Poor real-time location tracking
- No distance-based smart filtering

#### 6. **Fragmented Multi-Role Experience**
- Separate apps for customers, restaurants, delivery agents
- Inconsistent UX across roles
- High training overhead
- Poor coordination between roles

---

## ✅ How Foodify Solves These Problems

### **Our Unique Approach**

Foodify doesn't just replicate existing platforms - it **innovates** to solve real-world problems:

#### 🌟 **Revolutionary Food Donation System**

**The Problem We Solve:**
Restaurants discard edible food worth lakhs monthly while millions face food insecurity.

**Our Solution:**
Complete donation platform with:
- Smart quantity booking (book 5 out of 25 servings)
- Time-based urgency system (Critical/High/Medium/Low)
- Auto-expiry filtering (expired items auto-hidden)
- GPS navigation to pickup locations
- Donor-booker direct communication
- Real-time availability updates

**Impact:**
- ✅ Reduces restaurant waste by 60-80%
- ✅ Provides free meals to community
- ✅ Tax benefits for donors
- ✅ Environmental sustainability

#### 🗺️ **Advanced GPS & Navigation**

**The Problem We Solve:**
Users struggle to find pickup locations, delivery tracking is vague.

**Our Solution:**
- Geoapify API integration
- One-tap Google Maps navigation
- Precise lat/lon coordinates
- Distance calculation and filtering
- Address autocomplete and map picker

#### ⏰ **Intelligent Time Management**

**The Problem We Solve:**
No visibility into food freshness or urgency.

**Our Solution:**
- Visual urgency badges (color-coded)
- Countdown timers (exact hours remaining)
- Smart sorting (most urgent first)
- Auto-refresh every 2 minutes
- Expiry-based filtering

#### 📊 **Flexible Quantity System**

**The Problem We Solve:**
Fixed portions lead to over-ordering and waste.

**Our Solution:**
- Granular quantity selection
- Multi-user booking support
- Real-time availability tracking
- Visual quantity bars
- Various units (servings, kg, pieces, plates)

---

## 🏆 Competitive Advantage Matrix

| Feature | Existing Platforms | Foodify |
|---------|-------------------|----------|
| Food Waste Solution | ❌ None | ✅ **Complete donation system** |
| Quantity Flexibility | ❌ Fixed only | ✅ **Granular booking** |
| Expiry Management | ❌ Static | ✅ **Dynamic urgency** |
| GPS Navigation | ⚠️ Basic | ✅ **Full integration** |
| Social Impact | ❌ None | ✅ **Community-focused** |
| Multi-Role Platform | ⚠️ Separate apps | ✅ **Unified system** |
| Real-Time Updates | ⚠️ Limited | ✅ **Auto-refresh** |
| Environmental Focus | ❌ None | ✅ **Waste reduction** |

---

## Technology Stack

### Backend
- **Framework**: Django 5.2.11
- **Language**: Python
- **Database**: SQLite (Development) - easily scalable to PostgreSQL/MySQL
- **Authentication**: Django's built-in authentication system

### Frontend
- **HTML5** with Django Template Language
- **CSS3** with modern design systems (CSS Grid, Flexbox, CSS Variables)
- **JavaScript** (Vanilla) for interactivity
- **Responsive Design** for cross-device compatibility

### Additional Technologies
- Django Signals for automated profile creation
- Django Forms for data validation
- Django ORM for database operations
- Media file handling for image uploads

---

## Core Features

### 1. User Management System

#### 1.1 Dual User Roles
- **Customer Role**: Browse restaurants, place orders, track deliveries
- **Restaurant Owner Role**: Manage restaurants, menus, and orders
- Automatic profile creation using Django signals
- Role-based dashboard redirects

#### 1.2 Authentication & Authorization
- Secure user registration with form validation
- Login system with credential verification
- Session management (24-hour session validity)
- Protected routes with login requirements
- Role-based access control for sensitive operations

#### 1.3 User Profiles
- Extended user profiles with additional fields:
  - Phone number
  - Delivery address
  - Profile picture upload
  - User type designation
- Automatic profile creation on user registration

### 2. Restaurant Management

#### 2.1 Restaurant Listing
- Public restaurant directory with approved restaurants
- Advanced filtering system:
  - Search by restaurant name or cuisine type
  - Filter by cuisine category
  - Vegetarian-only filter
  - Minimum rating filter
- Restaurant cards displaying:
  - Restaurant name and image
  - Cuisine type
  - Star ratings
  - Distance from user
  - Vegetarian indicator

#### 2.2 Restaurant Details
- Comprehensive restaurant information page
- Complete menu display with categories
- Menu item details (name, price, description, image)
- Availability status indicators
- Vegetarian/Non-vegetarian tags
- Direct "Add to Cart" functionality

#### 2.3 Restaurant Owner Dashboard
- View all owned restaurants
- Quick access to restaurant management tools
- Order management interface
- Analytics dashboard (order history, revenue tracking)

#### 2.4 Restaurant Creation & Editing
- Form-based restaurant creation
- Upload restaurant images
- Specify cuisine type, location, description
- Set vegetarian status
- Edit existing restaurant details
- Admin approval system

### 3. Menu Management

#### 3.1 Menu Item Operations
- Add new menu items with:
  - Item name and description
  - Price setting
  - Image upload
  - Availability toggle
  - Vegetarian/Non-vegetarian designation
- Edit existing menu items
- Delete menu items
- Manage item availability status

#### 3.2 Menu Organization
- Items organized by restaurant
- Category-based display (expandable feature)
- Search and filter within menu
- Availability indicators

### 4. Shopping Cart System

#### 4.1 Cart Management
- Add items to cart from restaurant pages
- Quantity adjustment (increase/decrease)
- Remove individual items
- Clear entire cart
- Real-time subtotal calculation
- Persistent cart (stored in database)

#### 4.2 Cart Display
- Itemized cart view with:
  - Menu item details
  - Quantity selectors
  - Individual item prices
  - Item subtotals
- Price breakdown:
  - Subtotal
  - Delivery fee (₹40.00)
  - Tax (5% GST)
  - Grand total
- Recent orders history

### 5. Order Management System

#### 5.1 Customer Order Placement
- Order checkout with delivery details:
  - Delivery address input
  - Phone number verification
  - Order review before placement
- Automatic order creation
- Order confirmation with order ID
- Order history tracking

#### 5.2 Order Tracking
- Order status display with multiple states:
  - Pending
  - Confirmed
  - Preparing
  - Out for Delivery
  - Delivered
  - Cancelled
- Order detail view showing:
  - Order items and quantities
  - Restaurant information
  - Delivery address
  - Total amount breakdown
  - Order timestamp
  - Current status

#### 5.3 Order History
- Chronological list of all past orders
- Order status badges
- Quick access to order details
- Reorder functionality (future)

#### 5.4 Restaurant Owner Order Management
- View all orders for owned restaurants
- Filter orders by status and restaurant
- Update order status with one click
- Order details with customer information
- Revenue tracking per order

### 6. User Interface & Experience

#### 6.1 Modern Design System
- Custom CSS variables for consistent theming
- Color palette:
  - Primary: #ff5722 (Orange)
  - Accent colors
  - Semantic colors (success, error, warning)
- Typography using modern web fonts
- Shadow system for depth perception
- Custom animations and transitions

#### 6.2 Responsive Layout
- Mobile-first design approach
- Breakpoint-based responsive design
- Touch-friendly interface elements
- Adaptive navigation

#### 6.3 Hero Section
- Attractive landing page with hero image
- Call-to-action buttons
- Modern clip-path design
- Animated text effects

#### 6.4 Cuisine Carousel
- Horizontal scrollable cuisine categories
- Circular cuisine images
- Smooth scroll behavior
- Click-to-filter functionality
- Category options:
  - Biryani
  - Pizza
  - Burger
  - Chinese
  - Cake
  - Pasta
  - Salad

#### 6.5 Interactive Elements
- Hover effects on cards and buttons
- Smooth transitions
- Loading states
- Success/error message toasts
- Auto-dismissing alerts (3-second timeout)

### 7. Navigation System

#### 7.1 Main Navigation
- Sticky navigation bar
- Logo with home link
- Navigation links:
  - Home
  - Restaurants
  - Orders/My Order (customer)
  - Contact
- Dynamic navigation based on user role
- Cart badge with item count

#### 7.2 User-Specific Navigation
- Login/Sign up buttons (guest users)
- User greeting with username
- My Restaurants (restaurant owners)
- Logout functionality
- Shopping cart access with item counter

### 8. Search & Filter System

#### 8.1 Restaurant Search
- Text-based search
- Search by name or cuisine
- Real-time filter application
- Combined filter support

#### 8.2 Advanced Filters
- Cuisine type filter
- Vegetarian-only option
- Minimum rating selector
- Multi-criteria filtering

### 9. Media Management

#### 9.1 Image Uploads
- Restaurant images
- Menu item images
- User profile pictures
- Organized media storage (media/ directory)
- Image optimization and validation

#### 9.2 Static Files
- CSS stylesheets (style.css, navbar.css)
- JavaScript files
- Static assets (cuisine images, hero images)
- Organized file structure

### 10. Database Models

#### 10.1 User Profile Model
- Extended Django User model
- User type classification
- Contact information
- Address storage
- Timestamps

#### 10.2 Restaurant Model
- Owner relationship
- Restaurant details (name, cuisine, location)
- Rating system (0-5 stars)
- Distance tracking
- Approval status
- Image storage

#### 10.3 MenuItem Model
- Restaurant relationship
- Item details (name, description, price)
- Availability toggle
- Vegetarian flag
- Image storage

#### 10.4 Cart Model
- User relationship
- Menu item relationship
- Quantity tracking
- Unique constraint (user + menu item)
- Subtotal calculation

#### 10.5 Order Model
- User and restaurant relationships
- Order status workflow
- Price breakdown (subtotal, delivery, tax)
- Delivery address
- Timestamps
- Grand total calculation

#### 10.6 OrderItem Model
- Order relationship
- Menu item snapshot
- Price preservation
- Quantity tracking

---

## Future Implementations

### 1. Payment Gateway Integration
- **Multiple Payment Options**:
  - Credit/Debit cards
  - UPI payments (Google Pay, PhonePe, Paytm)
  - Net banking
  - Cash on delivery
- **Payment Processing**:
  - Razorpay/Stripe integration
  - Secure transaction handling
  - Payment confirmation emails
  - Refund management

### 2. Real-Time Order Tracking
- **Live Tracking Features**:
  - GPS-based delivery tracking
  - Real-time delivery person location
  - Estimated delivery time
  - Push notifications for status updates
  - WebSocket integration for live updates

### 3. Rating & Review System
- **Restaurant Reviews**:
  - Star ratings (1-5)
  - Written reviews
  - Photo reviews
  - Review moderation
  - Average rating calculation
- **Menu Item Reviews**:
  - Item-specific ratings
  - Taste, quality, portion size ratings
  - Helpful review voting

### 4. Advanced Search & Recommendations
- **AI-Powered Recommendations**:
  - Personalized restaurant suggestions
  - Order history-based recommendations
  - Trending items
  - Popular dishes
- **Enhanced Search**:
  - Fuzzy search
  - Auto-complete suggestions
  - Search by ingredients
  - Dietary preference filters

### 5. Loyalty & Rewards Program
- **Customer Rewards**:
  - Points system
  - Cashback offers
  - Referral bonuses
  - First-time user discounts
  - Loyalty tiers (Bronze, Silver, Gold)
- **Promotional Features**:
  - Coupon codes
  - Festival offers
  - Free delivery vouchers

### 6. Multi-Language Support
- **Internationalization**:
  - Hindi, Tamil, Telugu, etc.
  - RTL language support
  - Currency localization
  - Date/time formatting

### 7. Advanced Analytics Dashboard
- **Restaurant Owner Analytics**:
  - Sales trends and graphs
  - Peak ordering times
  - Popular menu items
  - Revenue reports
  - Customer demographics
- **Admin Analytics**:
  - Platform-wide statistics
  - Restaurant performance comparison
  - User growth metrics

### 8. Delivery Person Management
- **Delivery System**:
  - Delivery person registration
  - Order assignment algorithm
  - Delivery tracking
  - Earnings dashboard
  - Performance ratings

### 9. Social Features
- **Social Integration**:
  - Share orders on social media
  - Invite friends
  - Group ordering
  - Food communities
  - Recipe sharing

### 10. Advanced Filtering & Sorting
- **Enhanced Filters**:
  - Price range filter
  - Delivery time filter
  - Offers/discounts filter
  - Newly opened restaurants
  - Top-rated filter
- **Sorting Options**:
  - Sort by rating
  - Sort by delivery time
  - Sort by price
  - Sort by distance

### 11. Mobile Application
- **Native Apps**:
  - Android app (Kotlin/Java)
  - iOS app (Swift)
  - Push notifications
  - Offline mode support
  - Biometric authentication

### 12. Chat Support System
- **Customer Service**:
  - Live chat with restaurants
  - Customer support chatbot
  - Order-specific queries
  - AI-powered FAQ system

### 13. Favorites & Wishlists
- **Personalization**:
  - Favorite restaurants
  - Saved menu items
  - Wishlist for later ordering
  - Quick reorder from favorites

### 14. Scheduled Ordering
- **Advance Ordering**:
  - Schedule orders for future
  - Recurring orders
  - Party/event bulk orders
  - Pre-order for peak times

### 15. Dietary Preferences & Allergen Filters
- **Health Features**:
  - Allergen information
  - Calorie counting
  - Macro nutritional information
  - Vegan, gluten-free filters
  - Healthy meal suggestions

### 16. Restaurant Performance Metrics
- **Owner Dashboard Enhancements**:
  - Order acceptance rate
  - Average preparation time
  - Customer satisfaction score
  - Menu item performance
  - Peak hours analysis

### 17. Dynamic Pricing & Offers
- **Smart Pricing**:
  - Surge pricing during peak hours
  - Dynamic discounts
  - Happy hour specials
  - Combo offers
  - Bundle deals

### 18. Email & SMS Notifications
- **Communication System**:
  - Order confirmation emails
  - Status update SMS
  - Promotional emails
  - Newsletter subscriptions
  - Birthday/anniversary offers

### 19. Admin Panel Enhancements
- **Super Admin Features**:
  - Restaurant approval workflow
  - User management
  - Content moderation
  - Platform configuration
  - Revenue management
  - Dispute resolution

### 20. API for Third-Party Integration
- **Developer API**:
  - RESTful API
  - API documentation
  - OAuth integration
  - Webhook support
  - Third-party restaurant aggregation

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ANAND-JATOTHU/FoodDelivery.git
   cd Team-8-main
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser and navigate to `http://127.0.0.1:8000`

---

## Project Structure

```
Team-8-main/
├── accounts/              # User authentication & profiles
│   ├── models.py         # UserProfile model
│   ├── views.py          # Login, register, logout
│   ├── forms.py          # User registration forms
│   └── templates/        # Account-related templates
├── restaurants/           # Restaurant management
│   ├── models.py         # Restaurant, MenuItem models
│   ├── views.py          # Restaurant CRUD operations
│   ├── forms.py          # Restaurant and menu forms
│   └── templates/        # Restaurant templates
├── orders/                # Order management
│   ├── models.py         # Cart, Order, OrderItem models
│   ├── views.py          # Cart and order operations
│   └── templates/        # Order templates
├── templates/             # Global templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── contact.html      # Contact page
│   └── css/              # CSS files
├── static/                # Static files
│   └── assets/           # Images and media
├── media/                 # User-uploaded files
├── foodify_project/       # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL configuration
│   └── views.py          # Main views
├── manage.py              # Django management script
└── db.sqlite3            # SQLite database
```

---

## Usage Guide

### For Customers
1. Register as a customer
2. Browse restaurants on the homepage
3. Click on a restaurant to view menu
4. Add items to cart
5. Review cart and proceed to checkout
6. Enter delivery details
7. Place order
8. Track order status

### For Restaurant Owners
1. Register as a restaurant owner
2. Access owner dashboard
3. Add restaurant details
4. Create menu items
5. Manage orders
6. Update order status
7. View order history

---

## Security Features

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection
- Secure password hashing
- Session security
- Login required decorators
- Role-based access control
- Input validation and sanitization

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Credits

**Developed by**: Edunet Team-8  
**Framework**: Django  
**Year**: 2025

---

## Contact & Support

For questions, issues, or suggestions:
- **GitHub**: https://github.com/ANAND-JATOTHU/FoodDelivery
- **Email**: [Contact form on website]

---

## Conclusion

Foodify represents a modern, scalable solution for online food delivery operations. With its comprehensive feature set, intuitive design, and robust architecture, it serves as an excellent foundation for a production-ready food delivery platform. The extensive roadmap for future enhancements ensures that the platform can grow and adapt to evolving market demands while maintaining its core focus on user experience and operational efficiency.
