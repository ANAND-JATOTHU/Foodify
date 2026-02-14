from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    # Public views
    path('', views.donation_list, name='donation_list'),
    path('<int:donation_id>/', views.donation_detail, name='donation_detail'),
    
    # Donation creation and management
    path('donate/', views.donate_food, name='donate_food'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('<int:donation_id>/delete/', views.delete_donation, name='delete_donation'),
    
    # Booking system
    path('<int:donation_id>/book/', views.book_donation, name='book_donation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Donor management
    path('<int:donation_id>/bookings/', views.donor_bookings, name='donor_bookings'),
    path('booking/<int:booking_id>/collect/', views.mark_collected, name='mark_collected'),
    
    # API endpoints
    path('api/nearby/', views.get_donations_near_location, name='nearby_donations'),
]
