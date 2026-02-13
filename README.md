# 🍕 Foodify - Complete Food Delivery Platform

## Project Title
**Foodify: Multi-Role Food Delivery & Management System**

---

## Abstract

Foodify is a comprehensive, full-stack web-based food delivery and restaurant management platform built with Django and Python. The system provides a seamless experience for three distinct user roles: **Customers**, **Restaurant Owners**, and **Delivery Agents**. It features an intuitive user interface with real-time order tracking, integrated payment processing, food donation management, and delivery logistics.

The platform addresses the complete food delivery ecosystem by providing customers with easy restaurant browsing and ordering capabilities, restaurant owners with comprehensive management dashboards, and delivery agents with optimized delivery tracking tools. Additionally, Foodify incorporates a unique food donation feature to reduce food waste and support community welfare.

Key technologies include Django framework, SQLite database, Stripe payment integration, responsive HTML/CSS/JavaScript frontend, and AOS (Animate On Scroll) library for smooth animations.

---

## 🌟 Features & Functionalities

### 1. **Multi-Role Authentication System**
- **Three User Types**:
  - 🛍️ **Customer**: Browse restaurants, order food, track deliveries
  - 🏪 **Restaurant Owner**: Manage restaurants, menus, and orders
  - 🚴 **Delivery Agent**: Accept and deliver orders, manage availability
- **Secure Authentication**: Login/logout with session management
- **Dynamic Registration Form**: Conditional fields based on selected user type
- **Premium Animated Login UI**: 
  - Food-themed glassmorphism design
  - Floating food emoji animations
  - Password visibility toggle
  - Ripple effects on buttons
  - Responsive and accessible

### 2. **Customer Features**
- **Restaurant Browsing**:
  - Search by restaurant name or cuisine type
  - Filter by rating, distance, and dietary preferences (veg/non-veg)
  - View restaurant details and complete menus
  - Add restaurants to favorites
- **Shopping Cart Management**:
  - Add/remove/update menu items
  - Real-time price calculation with delivery fees and taxes
  - Cart badge showing item count
- **Order Placement**: 
  - Secure checkout process
  - Order history and tracking
  - Payment integration for online transactions
- **Home Page**:
  - Hero section with call-to-action
  - Cuisine carousel (Pizza, Burger, Biryani, etc.)
  - Featured food cards with smooth animations

### 3. **Restaurant Owner Features**
- **Owner Dashboard**:
  - View all owned restaurants
  - Quick access to restaurant management
  - Order notifications and management
- **Restaurant Management**:
  - Add new restaurants with details (cuisine, location, description)
  - Edit restaurant information and images
  - Approval system for restaurant listings
- **Menu Management**:
  - Add, edit, and delete menu items
  - Set item availability status
  - Upload food images
  - Categorize menu items (veg/non-veg)
- **Order Management**:
  - View incoming orders  
  - Update order status (confirmed, preparing, ready)
  - Track order history and revenue

### 4. **Delivery Agent Features**
- **Delivery Dashboard**:
  - View assigned orders
  - Filter by status (pending, active, delivered)
  - Track earnings and total deliveries
- **Order Management**:
  - Accept or reject order assignments
  - Update order status (out for delivery, delivered)
  - Real-time delivery tracking
- **Agent Profile**:
  - Vehicle details (type, number, license)
  - Availability status toggle
  - ID proof verification system

### 5. **Food Donation System**
- **Donate Surplus Food**:
  - Create donation listings with food details
  - Specify quantity, category (cooked/raw/packaged)
  - Set expiry times to ensure food safety
  - Upload proof images
- **Browse Donations**:
  - Search available food donations
  - Filter by category and food type
  - Reserve donations for pickup
  - Notification system for donors and receivers
- **Donation Management**:
  - Track donation status (available, reserved, collected)
  - Admin approval and verification
  - Reduce food waste and support community

### 6. **Payment System**
- **Stripe Integration**:
  - Secure online payment processing
  - Support for credit/debit cards
  - Payment status tracking
- **Django-Payments Framework**:
  - Multiple payment provider support
  - Payment transaction history
  - Automated payment notifications
- **Transaction Management**:
  - Detailed payment records
  - Refund processing
  - Restaurant-wise revenue tracking

### 7. **Search & Filtering**
- **Advanced Search**:
  - Search restaurants by name or cuisine
  - Multi-criteria filtering:
    - Cuisine type (Italian, Indian, Chinese, etc.)
    - Dietary preferences (Vegetarian/Non-Vegetarian)
    - Distance from user location
    - Restaurant ratings (4+ stars, 3+ stars)
  - Real-time search results
- **Smart Filtering**: Combine multiple filters for precise results

### 8. **Admin Panel**
- **Comprehensive Management**:
  - User management (customers, owners, agents)
  - Restaurant approval workflow
  - Order monitoring and analytics
  - Payment transaction oversight
  - Donation moderation
- **Model Administration**:
  - UserProfile (with user role tracking)
  - DeliveryAgent (vehicle and license details)
  - Restaurant and MenuItem
  - Orders and OrderItems
  - Payments and PaymentTransactions
  - Donations and DonationProofs
  - Notifications

### 9. **UI/UX Enhancements**
- **Responsive Design**: Mobile-first approach, works on all devices
- **Smooth Animations**:
  - AOS (Animate On Scroll) library integration
  - Slide-in, fade-in, zoom effects
  - Hover animations and transitions
- **Modern Design Elements**:
  - Glassmorphism effects
  - Gradient backgrounds
  - Card-based layouts
  - Icon-based navigation
- **Visual Feedback**:
  - Toast notifications for actions
  - Loading states
  - Success/error messages

### 10. **Additional Features**
- **Contact System**: Contact form for user inquiries
- **Profile Management**: Update user information and profile pictures
- **Session Management**: Secure login sessions with timeout
- **Media Uploads**: Support for restaurant and food images
- **Email Notifications**: Order confirmations and updates
- **RESTful URL Structure**: Clean and semantic URLs
- **CSRF Protection**: Security against cross-site attacks

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.11
- **Language**: Python 3.x
- **Database**: SQLite (Development) / PostgreSQL (Production-ready)
- **ORM**: Django ORM
- **Authentication**: Django Built-in Auth System

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties
- **JavaScript (Vanilla)**: Interactive features
- **AOS Library**: Scroll animations
- **Responsive Design**: Mobile-first approach

### Payment Integration
- **Stripe API**: Payment processing
- **Django-Payments**: Payment framework

### Additional Tools
- **Python Dotenv**: Environment variable management
- **Pillow**: Image processing
- **Django Messages Framework**: User notifications

---

## 📊 Database Schema

### Core Models

1. **User (Django Built-in)** - Base authentication
2. **UserProfile** - Extended user information
   - user_type: customer | restaurant_owner | delivery_agent
   - phone, profile_picture, address
3. **DeliveryAgent** - Delivery agent details
   - vehicle_type, vehicle_number, driving_license
   - availability_status, total_deliveries, earnings
4. **Restaurant** - Restaurant information
   - owner, name, cuisine, rating, location, distance
   - is_veg, is_approved
5. **MenuItem** - Restaurant menu items
   - restaurant, name, price, description, image
   - is_available, is_veg
6. **Cart** - Shopping cart items
   - user, menu_item, quantity
7. **Order** - Customer orders
   - user, restaurant, delivery_agent
   - total_amount, delivery_fee, tax_amount
   - status, delivery_address, payment details
8. **OrderItem** - Individual items in order
   - order, menu_item, name, price, quantity
9. **Payment** - Payment transactions
   - order, variant, status, amount
10. **PaymentTransaction** - Detailed payment records
   - order, restaurant, customer, transaction_id
   - payment_method, status, gateway_response
11. **Donation** - Food donations
   - donor, restaurant, food_name, quantity, category
   - status, expiry_time, reserved_by
12. **DonationProof** - Donation verification
   - donation, image, notes
13. **Notification** - User notifications
   - user, message, is_read, donation

---

## 🗂️ Project Structure

```
Foodify/
├── accounts/               # User authentication & profiles
│   ├── models.py          # UserProfile, DeliveryAgent models
│   ├── views.py           # Login, register, logout views
│   ├── forms.py           # Registration forms
│   └── templates/
│       └── accounts/
│           └── login_signup.html  # Premium animated login UI
├── restaurants/           # Restaurant management
│   ├── models.py          # Restaurant, MenuItem, Favorite
│   ├── views.py           # Restaurant list, search, CRUD
│   └── templates/
├── orders/                # Order management
│   ├── models.py          # Cart, Order, OrderItem, Payment
│   ├── views.py           # Cart, checkout, order tracking
│   └── templates/
├── payment_system/        # Payment processing
│   ├── models.py          # PaymentTransaction, Notifications
│   ├── views.py           # Payment processing views
│   └── templates/
├── donations/             # Food donation system
│   ├── models.py          # Donation, DonationProof, Notification
│   ├── views.py           # Donation CRUD, filter, reserve
│   └── templates/
├── delivery/              # Delivery agent features
│   ├── views.py           # Dashboard, order management
│   └── templates/
├── templates/             # Global templates
│   ├── base.html          # Base template with navbar
│   ├── index.html         # Homepage with hero & carousel
│   ├── contact.html       # Contact page
│   └── cart.html          # Shopping cart
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── assets/            # Images and media
├── media/                 # User uploads
├── foodify_project/       # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── views.py           # Core views (index, contact)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md              # Project documentation (this file)
└── db.sqlite3             # SQLite database
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (venv)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd Foodify
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - **Windows** (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Update Stripe API keys:
     ```
     STRIPE_PUBLIC_KEY=your_public_key_here
     STRIPE_SECRET_KEY=your_secret_key_here
     ```

6. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create Superuser (Admin Account)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Create Test Users** (Optional)
   ```bash
   python create_dummy_users.py
   ```
   This creates three test accounts:
   - **Customer**: username: `customer_user`, password: `customer123`
   - **Owner**: username: `owner_user`, password: `owner123`
   - **Agent**: username: `agent_user`, password: `agent123`

9. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

10. **Access the Application**
    - Homepage: http://localhost:8000/
    - Admin Panel: http://localhost:8000/admin/
    - Login: http://localhost:8000/accounts/login/

---

## 📱 Usage Guide

### For Customers
1. **Register/Login** at `/accounts/login/`
2. **Browse Restaurants** at `/restaurants/`
3. **Search & Filter**: Use search bar and filters
4. **Add to Cart**: Click menu items from restaurant details
5. **Checkout**: Review cart and complete payment
6. **Track Orders**: View order status and history

### For Restaurant Owners
1. **Register as Owner** with user_type "Restaurant Owner"
2. **Access Dashboard** at `/restaurants/dashboard/`
3. **Add Restaurant**: Fill in details and upload images
4. **Manage Menu**: Add/edit/delete menu items
5. **Process Orders**: View and update incoming orders

### For Delivery Agents
1. **Register as Agent** with vehicle details
2. **Access Dashboard** at `/delivery/dashboard/`
3. **Accept Orders**: View and accept assigned deliveries
4. **Update Status**: Mark orders as "Out for Delivery" or "Delivered"
5. **Toggle Availability**: Control when you receive orders

### Admin Functions
1. **Access Admin Panel** at `/admin/`
2. **Approve Restaurants**: Review and approve new listings
3. **Manage Users**: View and moderate user accounts
4. **Monitor Orders**: Track all platform orders
5. **Review Donations**: Approve food donation listings

---

## 🧪 Testing

### Manual Testing
- Login with test credentials for each user type
- Test complete order flow (browse → add to cart → checkout)
- Verify delivery agent workflow
- Test restaurant owner CRUD operations
- Check donation system functionality

### Automated Tests
```bash
python manage.py test
```

### Verify Authentication
```bash
python verify_auth.py
```

---

## 🔐 Security Features

- CSRF token protection on all forms
- Password hashing with Django's built-in system
- Session-based authentication
- SQL injection protection via Django ORM
- XSS prevention through template escaping
- Secure file upload validation
- Environment variable management for sensitive data

---

## 📈 Future Enhancements

- Real-time order tracking with maps integration
- Mobile app (iOS & Android)
- Advanced analytics dashboard for owners
- AI-based food recommendations
- Multi-language support
- Push notifications
- Loyalty rewards program
- Review and rating system enhancements
- Integration with multiple payment gateways

---

## 👥 Team & Contributors

**Developed by**: Edunet Team-8

**Project Lead**: [Your Name]

**Team Members**: [Team Member Names]

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Contact & Support

For queries, suggestions, or support:
- **Email**: support@foodify.com
- **Website**: www.foodify.com
- **GitHub**: [Your Repository URL]

---

## 🎯 Conclusion

Foodify is a complete, production-ready food delivery platform that demonstrates proficiency in full-stack web development, database design, payment integration, and modern UI/UX practices. The multi-role architecture makes it scalable and suitable for real-world deployment. The addition of the food donation feature showcases social responsibility and innovation beyond typical food delivery applications.

**Perfect for**: Academic projects, portfolio demonstration, startup MVP, or learning Django development.

---

**© 2025 Foodify | Designed with ❤️ for making food delivery seamless and intelligent**
