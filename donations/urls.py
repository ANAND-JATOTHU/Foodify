from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    # Public donation listing
    path('', views.donation_list, name='donation_list'),
    path('<int:donation_id>/', views.donation_detail, name='donation_detail'),
    
    # Create donation
    path('donate/', views.donate_food, name='donate_food'),
    
    # Booking management
    path('<int:donation_id>/book/', views.book_donation, name='book_donation'),
    path('<int:donation_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('<int:donation_id>/collected/', views.mark_as_collected, name='mark_as_collected'),
    path('<int:donation_id>/delete/', views.delete_donation, name='delete_donation'),
    
    # User dashboards  
    path('my-donations/', views.my_donations, name='my_donations'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Backward compatibility
    path('ngo-dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
]
