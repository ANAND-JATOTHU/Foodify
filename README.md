# 🍕 Foodify - Complete Food Delivery Platform

[![Django](https://img.shields.io/badge/Django-5.2.11-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Foodify** is a comprehensive, full-stack food delivery and donation platform built with Django. It features multi-role authentication, real-time order tracking, Stripe payments, GPS navigation, and an innovative food donation system to reduce waste.

---

## 🎯 Problem Statement & Our Solution

### Problems with Existing Food Delivery Platforms

Major food delivery platforms like **Zomato**, **Swiggy**, **UberEats**, and **DoorDash** have revolutionized food ordering, but they have critical gaps:

#### 1. **Food Waste Crisis** 🗑️
- **Problem**: Restaurants discard **30-40% of prepared food** daily (excess inventory, cancelled orders, near-expiry items)
- **Impact**: Environmental damage, lost revenue for restaurants, missed opportunities to help those in need
- **Existing Platforms**: No mechanism to redistribute surplus food; everything goes to waste

#### 2. **Lack of Social Responsibility Features** 💔
- **Problem**: Pure profit-driven models with no focus on community welfare or food security
- **Impact**: Food insecurity affects millions while edible food is discarded
- **Existing Platforms**: No donation/sharing features for surplus food

#### 3. **Poor Delivery Tracking** 📍
- **Problem**: Vague "15-20 mins away" estimates without real-time GPS visualization
- **Impact**: Customer frustration, missed deliveries, unclear agent locations
- **Existing Platforms**: Limited real-time tracking, no easy navigation for customers to pickup points

#### 4. **Rigid Quantity Systems** 🍽️
- **Problem**: Fixed portion sizes with no flexibility for sharing or partial bookings
- **Impact**: Users forced to order more than needed, contributing to waste
- **Existing Platforms**: No quantity-based partial booking systems

#### 5. **Limited Expiry Management** ⏰
- **Problem**: No time-based urgency indicators for perishable items or time-sensitive deals
- **Impact**: Users miss fresh food opportunities, restaurants can't clear inventory urgently
- **Existing Platforms**: Static listings with no urgency visualization

#### 6. **Complex Multi-Role Management** 👥
- **Problem**: Separate apps/interfaces for customers, restaurants, and delivery agents
- **Impact**: Fragmented experience, poor coordination, training overhead
- **Existing Platforms**: Multiple platforms with inconsistent UX

---

### 🚀 How Foodify Solves These Problems

#### ✅ **Revolutionary Food Donation System**

**Our Solution:**
- **Zero-Waste Platform**: Turn surplus food into community support
- **Smart Quantity Booking**: Book exactly what you need (e.g., "5 out of 25 servings")
- **Time-Based Expiry Management**: 
  - 🔥 **Critical** (< 2hrs): Pulsing red badge, highest priority
  - ⚠️ **High** (2-6hrs): Orange badge, urgent action needed
  - ⏰ **Medium** (6-12hrs): Yellow badge, available today
  - ✅ **Low** (> 12hrs): Green badge, fresh listing
- **GPS Navigation**: Direct routes to pickup locations via Google Maps
- **Donor-Booker Communication**: Contact details shared after booking
- **Auto-Expiry Filtering**: Expired items automatically hidden

**Real-World Impact:**
- Restaurants reduce waste and gain tax benefits
- Community members access free, quality food
- Environmental impact reduced (less landfill waste)
- Social responsibility integrated into platform

#### ✅ **Unified Multi-Role Platform**

**Our Solution:**
- Single platform for all user types (customers, owners, agents)
- Role-based dashboards with seamless transitions
- Consistent UX across all interfaces
- Reduced training time and support overhead

**Benefits:**
- Customers, owners, and agents use one app
- Easy role switching (e.g., customer can also donate)
- Lower platform maintenance costs

#### ✅ **Advanced GPS & Location Services**

**Our Solution:**
- **Geoapify Integration**: Real-time GPS location services
- **Smart Address Picker**: GPS auto-detect or manual map selection
- **Navigation Features**: 
  - One-tap navigation to pickup locations
  - Distance calculation from user location
  - Route optimization via Google Maps
- **Location Accuracy**: Precise lat/lon coordinates for all listings

**Benefits:**
- No more "lost delivery agent" confusion
- Easy navigation to donation pickup points
- Accurate distance-based filtering

#### ✅ **Transparent Time Management**

**Our Solution:**
- Visual urgency indicators (color-coded badges)
- Countdown timers showing exact hours remaining
- Auto-refresh every 2 minutes for real-time availability
- Expiry-based smart sorting (most urgent first)

**Benefits:**
- Users know exactly when food expires
- Urgent items get priority visibility
- Reduced food waste through time awareness

#### ✅ **Flexible Quantity System**

**Our Solution:**
- Granular quantity selection (servings, kg, pieces, plates, packets)
- Real-time availability updates as bookings are made
- Visual quantity bars showing available vs. booked portions
- Multi-user booking support (same donation, multiple bookers)

**Benefits:**
- Book exactly what you need
- Multiple people can share large donations
- Reduced over-ordering and waste

---

### 📊 Competitive Advantage Summary

| Feature | Zomato/Swiggy | UberEats | **Foodify** |
|---------|---------------|----------|-------------|
| **Food Donation System** | ❌ None | ❌ None | ✅ **Full-featured** |
| **Quantity-Based Booking** | ❌ Fixed portions | ❌ Fixed portions | ✅ **Flexible quantities** |
| **Time-Based Expiry** | ❌ Static | ❌ Static | ✅ **Dynamic urgency levels** |
| **GPS Navigation** | ⚠️ Limited | ⚠️ Limited | ✅ **Full GPS + Maps** |
| **Multi-Role Platform** | ⚠️ Separate apps | ⚠️ Separate apps | ✅ **Unified platform** |
| **Social Impact** | ❌ None | ❌ None | ✅ **Community-focused** |
| **Real-Time Updates** | ⚠️ Basic | ⚠️ Basic | ✅ **Auto-refresh, live tracking** |
| **Payment Integration** | ✅ Multiple | ✅ Multiple | ✅ **Stripe + Django-Payments** |

---

## 📋 Table of Contents

- [Features](#-features--functionalities)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Integration](#-api-integration)
- [Security](#-security-features)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Features & Functionalities

### 1. **Multi-Role Authentication System**

- **🛍 Customer**: Browse, order, track deliveries
- **🏪 Restaurant Owner**: Manage restaurants, menus, orders
- **🚴 Delivery Agent**: Accept/deliver orders, track earnings
- Premium animated login UI with glassmorphism
- Session-based authentication with role-based dashboards

### 2. **Enhanced Food Donation System** 🆕

**Solving the Food Waste Crisis - Our Most Innovative Feature**

Foodify's donation system is a **game-changer** that addresses the **30-40% food waste** problem plaguing the restaurant industry:

#### 🎯 **Core Features**

1. **Smart Quantity-Based Booking**
   - Book exactly what you need: "5 out of 25 servings"
   - Multiple users can book from same donation
   - Real-time availability updates
   - Prevents over-booking and ensures fair distribution
   - Supports various units: servings, kg, pieces, plates, packets

2. **Intelligent Time-Based Expiry System**
   - **Auto-Expiry Filtering**: Expired donations automatically hidden
   - **Visual Urgency Levels**:
     - 🔥 **Critical** (< 2 hours): Pulsing red badge, top priority
     - ⚠️ **High** (2-6 hours): Orange badge, urgent pickup needed
     - ⏰ **Medium** (6-12 hours): Yellow badge, pickup today
     - ✅ **Low** (> 12 hours): Green badge, fresh listing
   - **Countdown Timers**: Shows exact hours/minutes remaining
   - **Smart Sorting**: Most urgent donations appear first
   - **Auto-Refresh**: Page refreshes every 2 minutes for accuracy

3. **GPS-Powered Navigation & Location Services**
   - **Precise Location Tracking**: Lat/lon coordinates for all donations
   - **One-Tap Navigation**: Direct Google Maps integration
   - **Route Calculation**: Automatic route from your location to pickup
   - **Distance Display**: See how far donations are from you
   - **Address Autocomplete**: Easy address entry for donors
   - **Map Picker**: Visual location selection on interactive map

4. **Seamless Donor-Booker Communication**
   - **Contact Sharing**: Phone numbers exchanged after booking
   - **Booking Notifications**: Real-time alerts for donors
   - **Booking Details**: Booker name, phone, quantity, preferred time
   - **Collection Confirmation**: Donors mark items as collected
   - **Booking History**: Track all past bookings

5. **Professional Modern UI**
   - **Card-Based Layout**: Beautiful donation cards with images
   - **Advanced Filtering**:
     - Search by food name, location, tags
     - Filter by food type (Veg/Non-Veg/Vegan)
     - Filter by category (Cooked/Raw/Packaged/Baked)
     - Sort by urgency, quantity, or newest
   - **Visual Indicators**:
     - Quantity progress bars
     - Urgency color coding
     - Availability percentages
   - **Responsive Design**: Works perfectly on mobile and desktop

6. **Booking Management System**
   - **My Bookings Dashboard**: View all your bookings
   - **Status Tracking**: Pending → Confirmed → Collected
   - **Cancel Functionality**: Cancel bookings, quantity restored
   - **Navigation Button**: GPS directions from bookings page
   - **Booking Limits**: Validation to prevent over-booking

#### 🔄 **Complete Donation Workflow**

**For Donors (Restaurants/Individuals):**
1. Click "📦 Donate Food" button
2. Fill donation form:
   - Food name and description
   - Original quantity and unit
   - Food type (Veg/Non-Veg/Vegan)
   - Category (Cooked/Raw/Packaged/Baked)
   - Expiry date & time
   - Pickup location (with GPS/map picker)
   - Contact phone number
   - Optional: prepared time, pickup instructions, tags
3. Upload food image
4. Submit for listing
5. Receive booking notifications
6. Share contact details with bookers
7. Mark items as collected

**For Receivers (Community Members):**
1. Browse donations at `/donations/`
2. Use filters to find suitable food:
   - Search by name/location
   - Filter by veg/non-veg, category
   - Sort by urgency (expiring soon first)
3. View donation details:
   - Food description
   - Available quantity
   - Time remaining
   - Location with distance
4. Click "Book Now"
5. Select quantity needed
6. Enter contact details
7. Confirm booking
8. Receive confirmation with:
   - Donor's contact number
   - Pickup location address
   - Time remaining to collect
9. Navigate to pickup using GPS
10. Collect food and confirm

#### 📈 **Real-World Impact**

- **Environmental**: Reduces food waste going to landfills
- **Social**: Provides free meals to those in need
- **Economic**: Tax benefits for donors, savings for receivers
- **Community**: Builds connections between donors and community

#### 💡 **Technical Implementation Highlights**

- **Models**: `Donation`, `DonationBooking`, `DonationProof`, `Notification`
- **Auto-Expiry**: Background task checks expiry every 2 minutes
- **Quantity Tracking**: Real-time updates to `available_quantity`
- **Location Services**: Geoapify API for geocoding and navigation
- **Notifications**: In-app notifications for booking events
- **Security**: Validated inputs, authenticated actions only

### 3. **Customer Features**

- **Restaurant Discovery**:
  - Search by name/cuisine
  - Advanced filters (rating, distance, dietary preferences)
  - Cuisine carousel (Pizza, Burger, Biryani, Chinese, etc.)
- **Smart Cart**:
  - Real-time price calculation
  - Delivery fees (₹40) + 5% GST
  - Cart persistence
- **Order Tracking**:
  - Status updates (Pending → Confirmed → Preparing → Out for Delivery → Delivered)
  - Order history
  - Reorder functionality

### 4. **Restaurant Owner Dashboard**

- **Restaurant Management**:
  - Add/edit restaurants with images
  - Approval workflow
  - Location-based listing
- **Menu Management**:
  - CRUD operations on menu items
  - Veg/Non-veg tagging
  - Availability toggles
- **Order Processing**:
  - Real-time notifications
  - Status updates
  - Revenue tracking

### 5. **Delivery Agent Features**

- **Smart Dashboard**:
  - Assigned orders view
  - Earnings tracker
  - Delivery statistics
- **Order Management**:
  - Accept/reject assignments
  - Update delivery status
  - Performance metrics
- **Profile Management**:
  - Vehicle details
  - Availability toggle
  - License verification

### 6. **Payment System**

- **Stripe Integration**:
  - Secure card payments
  - Payment status tracking
  - Transaction history
- **Django-Payments Framework**:
  - Multiple provider support
  - Refund processing
  - Automated notifications

### 7. **Location Services** 🆕

- **Geoapify Integration**:
  - GPS geolocation
  - Address autocomplete
  - Map picker for manual selection
  - Reverse geocoding
- **Navigation Features**:
  - Google Maps integration
  - Route calculation
  - Distance tracking
- **Implementation**:
  - Cart page: GPS/map picker for delivery address
  - Donations: Navigate to pickup locations
  - Restaurants: Location-based filtering

### 8. **Modern UI/UX**

- **Responsive Design**: Mobile-first, all devices
- **Smooth Animations**:
  - AOS (Animate On Scroll) library
  - Hover effects and transitions
  - Loading states
- **Design Elements**:
  - Glassmorphism
  - Gradient backgrounds
  - Card-based layouts
  - Premium color schemes

---

## 🛠️ Technology Stack

### Backend
- **Django 5.2.11** - Web framework
- **Python 3.8+** - Programming language
- **SQLite** - Database (production-ready for PostgreSQL/MySQL)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling (Grid, Flexbox, Variables)
- **JavaScript** - Vanilla + ES6
- **AOS Library** - Scroll animations

### APIs & Integrations
- **Stripe API** - Payment processing
- **Geoapify API** - Maps, geocoding, navigation
- **Google Maps** - Navigation routes

### Additional
- **Python Dotenv** - Environment management
- **Pillow** - Image processing
- **Django Messages** - Notifications

---

## 📊 Database Schema

### Core Models

```python
# User Management
- User (Django built-in)
- UserProfile (customer/owner/agent + phone, address, picture)
- DeliveryAgent (vehicle details, license, availability, earnings)

# Restaurant System
- Restaurant (owner, name, cuisine, rating, location, approved status)
- MenuItem (restaurant, name, price, description, image, veg/non-veg)
- Favorite (user favorites)

# Order System
- Cart (user, menu_item, quantity)
- Order (user, restaurant, agent, amounts, status, delivery info)
- OrderItem (order, menu_item, quantity, price snapshot)

# Payment System
- Payment (order, variant, status, amount)
- PaymentTransaction (transaction_id, method, gateway response)

# Donation System (Enhanced) 🆕
- Donation (donor, food_name, original_quantity, available_quantity,
           quantity_unit, expiry_time, location, lat/lon, contact)
- DonationBooking (donation, booked_by, quantity_booked, booker_name,
                   booker_phone, status, preferred_collection_time)
- DonationProof (donation, image, notes, verified)
- Notification (user, donation, message, is_read)
```

### Key Relationships
- One User → Many Orders/Donations/Bookings
- One Restaurant → Many MenuItems/Orders
- One Order → Many OrderItems
- One Donation → Many DonationBookings

---

## 🗂️ Project Structure

```
Foodify/
├── accounts/              # Authentication & profiles
│   ├── models.py         # UserProfile, DeliveryAgent
│   ├── views.py          # Login, register, logout
│   └── templates/
│       └── login_signup.html  # Premium animated login
├── restaurants/           # Restaurant management
│   ├── models.py         # Restaurant, MenuItem, Favorite
│   ├── views.py          # CRUD, search, filtering
│   └── templates/
├── orders/                # Order & cart management
│   ├── models.py         # Cart, Order, OrderItem
│   ├── views.py          # Cart, checkout, tracking
│   └── templates/
│       └── cart.html     # GPS/map picker integration
├── payment_system/        # Payment processing
│   ├── models.py         # PaymentTransaction
│   ├── views.py          # Stripe integration
│   └── templates/
├── donations/             # Food donation system 🆕
│   ├── models.py         # Donation, DonationBooking, Proof
│   ├── views.py          # Quantity booking, expiry filtering
│   ├── forms.py          # DonationForm, BookingForm
│   └── templates/
│       ├── donation_list.html      # Modern cards with urgency
│       ├── book_donation.html      # Quantity selector
│       └── my_bookings.html        # GPS navigation
├── delivery/              # Delivery agent features
│   └── templates/
├── static/                # Static assets
│   ├── css/              # Stylesheets
│   ├── js/
│   │   └── geoapify.js   # Geoapify utilities
│   └── assets/           # Images
├── templates/             # Global templates
│   ├── base.html         # Base with navbar
│   ├── index.html        # Homepage with carousel
│   └── contact.html
├── media/                 # User uploads
├── foodify_project/       # Configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   └── context_processors.py  # Geoapify API key
├── manage.py
├── requirements.txt
├── .env                   # Environment variables
├── .env.example          # Template
├── populate_donations.py  # 10 dummy donations script
├── README.md             # This file
└── db.sqlite3
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ANAND-JATOTHU/Foodify.git
   cd Foodify
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env with your keys:
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   GEOAPIFY_API_KEY=your_geoapify_api_key
   ```

6. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Create Test Data** (Optional)
   ```bash
   # Create test users (customer, owner, agent)
   python create_test_accounts.py
   
   # Populate 10 dummy donations
   python populate_donations.py
   
   # Add sample restaurants
   python add_sample_restaurants.py
   ```

9. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

10. **Access Application**
    - Homepage: http://localhost:8000/
    - Admin: http://localhost:8000/admin/
    - Donations: http://localhost:8000/donations/
    - Login: http://localhost:8000/accounts/login/

---

## 📱 Usage Guide

### For Customers

1. **Register/Login** → `/accounts/login/`
2. **Browse Restaurants** → `/restaurants/`
3. **Search & Filter** → Use cuisine, veg/non-veg, rating filters
4. **Add to Cart** → Click items from restaurant details
5. **Use GPS** → Cart page has "Use GPS Location" button
6. **Checkout** → Review cart, enter delivery address
7. **Track Orders** → View status updates
8. **Browse Donations** → `/donations/` for free food
9. **Book Donation** → Select quantity, view GPS navigation

### For Restaurant Owners

1. **Register as Owner** → Select "Restaurant Owner" type
2. **Dashboard** → `/restaurants/dashboard/`
3. **Add Restaurant** → Fill details, upload images
4. **Manage Menu** → Add/edit items with prices
5. **Process Orders** → Update status (confirmed → preparing → ready)
6. **Donate Food** → Create donation listings for surplus

### For Delivery Agents

1. **Register as Agent** → Provide vehicle/license details
2. **Dashboard** → `/delivery/dashboard/`
3. **Accept Orders** → View assigned deliveries
4. **Update Status** → Mark "Out for Delivery" → "Delivered"
5. **Track Earnings** → View total deliveries & earnings

### Admin Functions

1. **Admin Panel** → `/admin/`
2. **Approve Restaurants** → Review new listings
3. **Manage Users** → View profiles, moderate
4. **Monitor Orders** → Track platform-wide orders
5. **Review Donations** → Approve listings, verify proofs

---

## 🔌 API Integration

### Geoapify API

Used for location services throughout the platform:

**Features:**
- GPS geolocation
- Address autocomplete
- Reverse geocoding
- Map display
- Distance calculation

**Implementation:**
```javascript
// static/js/geoapify.js
class GeoapifyUtils {
  async getCurrentLocation()      // Get user GPS
  async reverseGeocode(lat, lon)  // Coords to address
  initAutocomplete(input, onSelect)  // Address suggestions
  calculateDistance(lat1, lon1, lat2, lon2)  // Distance calc
}
```

**Usage:**
- Cart page: Pick delivery address
- Donations: Navigate to pickup
- Restaurants: Location-based filtering

### Stripe API

Secure payment processing:

**Features:**
- Card payments
- Payment intents
- Webhook handling
- Transaction tracking

---

## 🔐 Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing (Django's Argon2)
- ✅ Session-based authentication
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection (template escaping)
- ✅ Secure file uploads with validation
- ✅ Environment variables for sensitive data
- ✅ Role-based access control
- ✅ Input sanitization
- ✅ HTTPS-ready (in production)

---

## 🧪 Testing

### Manual Testing

**Test Accounts:**
```
Customer: username: customer_user, password: customer123
Owner:    username: owner_user,    password: owner123
Agent:    username: agent_user,    password: agent123
```

**Test Flows:**
1. Customer order flow (browse → cart → checkout)
2. Donation booking flow (list → book → navigate)
3. Restaurant owner workflow (add restaurant → menu → orders)
4. Delivery agent workflow (accept → deliver)

### Run Automated Tests
```bash
python manage.py test
```

### Verify Authentication
```bash
python verify_auth.py
```

---

## 📈 Future Enhancements

- [ ] Real-time WebSocket order tracking
- [ ] Mobile apps (iOS & Android)
- [ ] AI-based food recommendations
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Push notifications
- [ ] Loyalty rewards program
- [ ] Review & rating system enhancements
- [ ] Video reviews
- [ ] Chatbot customer support

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👥 Team & Contributors

**Developed by**: Edunet Team-8  
**GitHub**: [ANAND-JATOTHU](https://github.com/ANAND-JATOTHU)  
**Year**: 2025

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact & Support

- **GitHub**: https://github.com/ANAND-JATOTHU/Foodify
- **Email**: support@foodify.com
- **Issues**: Report bugs or request features via GitHub Issues

---

## 🎯 Conclusion

Foodify is a **production-ready**, comprehensive food delivery platform that demonstrates:
- ✅ Full-stack web development proficiency
- ✅ Complex database design and ORM usage
- ✅ Third-party API integrations (Stripe, Geoapify)
- ✅ Modern UI/UX best practices
- ✅ Social impact (food waste reduction)
- ✅ Scalable architecture

**Perfect for**: Portfolio projects, academic demonstrations, startup MVPs, learning Django development.

---

**© 2026 Foodify | Designed with ❤️ for seamless food delivery and waste reduction**
