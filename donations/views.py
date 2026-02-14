from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from .models import Donation, DonationBooking, DonationProof, Notification
from .forms import DonationForm, DonationBookingForm, DonationProofForm


def donation_list(request):
    """Public listing of available food donations with expiry filtering"""
    # Filter out expired donations automatically
    donations = Donation.objects.filter(
        expiry_time__gt=timezone.now()
    ).select_related('donor', 'restaurant').exclude(
        status__in=['expired', 'cancelled', 'collected']
    )
    
    # Search
    search = request.GET.get('search', '')
    if search:
        donations = donations.filter(
            Q(food_name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Filters
    food_type = request.GET.get('food_type', '')
    if food_type:
        donations = donations.filter(food_type=food_type)
    
    category = request.GET.get('category', '')
    if category:
        donations = donations.filter(category=category)
    
    # Sort by urgency (expiring soon first)
    sort = request.GET.get('sort', 'urgency')
    if sort == 'urgency':
        donations = donations.order_by('expiry_time')
    elif sort == 'quantity':
        donations = donations.order_by('-available_quantity')
    elif sort == 'newest':
        donations = donations.order_by('-created_at')
    else:
        donations = donations.order_by('expiry_time')
    
    context = {
        'donations': donations,
        'search_query': search,
        'food_type': food_type,
        'category': category,
        'sort': sort,
        'GEOAPIFY_API_KEY': settings.GEOAPIFY_API_KEY,
    }
    return render(request, 'donations/donation_list.html', context)


def donation_detail(request, donation_id):
    """Detailed view of a donation with map and booking"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Get active bookings for this donation
    bookings = donation.bookings.filter(
        booking_status__in=['pending', 'confirmed']
    ).select_related('booked_by')
    
    # Check if current user has already booked this
    user_booking = None
    if request.user.is_authenticated:
        user_booking = bookings.filter(booked_by=request.user).first()
    
    context = {
        'donation': donation,
        'bookings': bookings,
        'user_booking': user_booking,
        'is_donor': request.user == donation.donor if request.user.is_authenticated else False,
        'GEOAPIFY_API_KEY': settings.GEOAPIFY_API_KEY,
    }
    return render(request, 'donations/donation_detail.html', context)


@login_required
def donate_food(request):
    """Create a new food donation"""
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            
            # If user is a restaurant owner, auto-link restaurant
            if hasattr(request.user, 'profile') and request.user.profile.is_restaurant_owner:
                from restaurants.models import Restaurant
                try:
                    donation.restaurant = Restaurant.objects.filter(owner=request.user).first()
                except:
                    pass
            
            donation.save()
            messages.success(request, '✅ Food donation created successfully! Thank you for helping reduce food waste.')
            return redirect('donations:donation_detail', donation.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form with user's info if available
        initial = {}
        if hasattr(request.user, 'profile'):
            if request.user.profile.phone:
                initial['contact_phone'] = request.user.profile.phone
            initial['contact_name'] = request.user.get_full_name() or request.user.username
        form = DonationForm(initial=initial)
    
    context = {
        'form': form,
        'GEOAPIFY_API_KEY': settings.GEOAPIFY_API_KEY,
    }
    return render(request, 'donations/donate_food.html', context)


@login_required
def book_donation(request, donation_id):
    """Book a donation with quantity selection"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Check if donation is available
    if not donation.is_available:
        messages.error(request, '❌ This donation is no longer available.')
        return redirect('donations:donation_detail', donation_id)
    
    # Check if user is trying to book their own donation
    if donation.donor == request.user:
        messages.error(request, '❌ You cannot book your own donation.')
        return redirect('donations:donation_detail', donation_id)
    
    if request.method == 'POST':
        form = DonationBookingForm(request.POST, donation=donation, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.donation = donation
            booking.booked_by = request.user
            booking.save()
            
            # Update donation available quantity
            donation.available_quantity -= booking.quantity_booked
            donation.update_status()
            
            # Create notification for donor
            Notification.objects.create(
                user=donation.donor,
                donation=donation,
                message=f"🎉 {booking.booker_name} booked {booking.quantity_booked} {donation.quantity_unit} of your {donation.food_name}. Contact: {booking.booker_phone}"
            )
            
            messages.success(
                request, 
                f'✅ Successfully booked {booking.quantity_booked} {donation.quantity_unit}! '
                f'Pickup location: {donation.location}. Contact: {donation.contact_phone}'
            )
            return redirect('donations:my_bookings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DonationBookingForm(donation=donation, user=request.user)
    
    context = {
        'form': form,
        'donation': donation,
        'GEOAPIFY_API_KEY': settings.GEOAPIFY_API_KEY,
    }
    return render(request, 'donations/book_donation.html', context)


@login_required
def my_donations(request):
    """List user's donations and manage them"""
    donations = Donation.objects.filter(donor=request.user).annotate(
        total_booked=Sum('bookings__quantity_booked')
    ).order_by('-created_at')
    
    context = {
        'donations': donations,
    }
    return render(request, 'donations/my_donations.html', context)


@login_required
def my_bookings(request):
    """List user's bookings"""
    bookings = DonationBooking.objects.filter(
        booked_by=request.user
    ).select_related('donation', 'donation__donor').order_by('-booked_at')
    
    context = {
        'bookings': bookings,
        'GEOAPIFY_API_KEY': settings.GEOAPIFY_API_KEY,
    }
    return render(request, 'donations/my_bookings.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking and restore quantity"""
    booking = get_object_or_404(DonationBooking, id=booking_id, booked_by=request.user)
    
    if not booking.is_active:
        messages.error(request, '❌ This booking cannot be cancelled.')
        return redirect('donations:my_bookings')
    
    if request.method == 'POST':
        if booking.cancel():
            messages.success(request, '✅ Booking cancelled successfully. Quantity restored to donation.')
        else:
            messages.error(request, '❌ Unable to cancel booking.')
        return redirect('donations:my_bookings')
    
    context = {'booking': booking}
    return render(request, 'donations/cancel_booking.html', context)


@login_required
def donor_bookings(request, donation_id):
    """View all bookings for a donation (donor only)"""
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    bookings = donation.bookings.all().select_related('booked_by').order_by('-booked_at')
    
    context = {
        'donation': donation,
        'bookings': bookings,
    }
    return render(request, 'donations/donor_bookings.html', context)


@login_required
def mark_collected(request, booking_id):
    """Mark a booking as collected (donor only)"""
    booking = get_object_or_404(DonationBooking, id=booking_id)
    
    # Verify user is the donor
    if booking.donation.donor != request.user:
        messages.error(request, '❌ You are not authorized to perform this action.')
        return redirect('donations:my_donations')
    
    if request.method == 'POST':
        booking.mark_collected()
        messages.success(request, f'✅ Marked booking by {booking.booker_name} as collected.')
        return redirect('donations:donor_bookings', booking.donation.id)
    
    context = {'booking': booking}
    return render(request, 'donations/mark_collected.html', context)


@login_required
def delete_donation(request, donation_id):
    """Delete a donation (only if no active bookings)"""
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    
    # Check for active bookings
    active_bookings = donation.bookings.filter(booking_status__in=['pending', 'confirmed']).count()
    if active_bookings > 0:
        messages.error(request, f'❌ Cannot delete donation with {active_bookings} active booking(s).')
        return redirect('donations:my_donations')
    
    if request.method == 'POST':
        donation.status = 'cancelled'
        donation.save()
        messages.success(request, '✅ Donation cancelled successfully.')
        return redirect('donations:my_donations')
    
    context = {'donation': donation}
    return render(request, 'donations/delete_donation.html', context)


def get_donations_near_location(request):
    """API endpoint to get donations near a location"""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    radius_km = float(request.GET.get('radius', 5))
    
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and longitude required'}, status=400)
    
    # Simple bounding box query (for more accuracy, use geospatial database)
    donations = Donation.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        expiry_time__gt=timezone.now(),
        status__in=['available', 'partially_booked']
    )
    
    donations_data = [
        {
            'id': d.id,
            'food_name': d.food_name,
            'quantity': f"{d.available_quantity} {d.quantity_unit}",
            'latitude': float(d.latitude),
            'longitude': float(d.longitude),
            'urgency': d.urgency_level,
            'hours_left': round(d.hours_until_expiry, 1),
        }
        for d in donations
    ]
    
    return JsonResponse({'donations': donations_data})
