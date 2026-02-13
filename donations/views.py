from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import Donation, DonationProof, Notification
from .forms import DonationForm, DonationProofForm
from orders.models import Order, OrderItem


def donation_list(request):
    """Public listing of available food donations with search and filters"""
    donations = Donation.objects.select_related('donor', 'restaurant').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        donations = donations.filter(
            Q(food_name__icontains=search) |
            Q(description__icontains=search) |
            Q(address__icontains=search)
        )
    
    # Filters
    food_type = request.GET.get('food_type', '')
    if food_type:
        donations = donations.filter(food_type=food_type)
    
    category = request.GET.get('category', '')
    if category:
        donations = donations.filter(category=category)
    
    status = request.GET.get('status', '')
    if status:
        donations = donations.filter(status=status)
    else:
        # By default, show only available and booked donations
        donations = donations.filter(status__in=['available', 'booked'])
    
    min_serving = request.GET.get('min_serving', '')
    if min_serving:
        try:
            donations = donations.filter(serving_count__gte=int(min_serving))
        except ValueError:
            pass
    
    # Order by created_at
    donations = donations.order_by('-created_at')
    
    context = {
        'donations': donations,
        'search_query': search,
        'food_type': food_type,
        'category': category,
        'status': status,
        'min_serving': min_serving,
    }
    return render(request, 'donations/donation_list.html', context)


def donation_detail(request, donation_id):
    """Detailed view of a donation with map"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    context = {
        'donation': donation,
        'geoapify_api_key': 'e0f8bf51ccb649ea846a4ff8312d98cb',
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
            if request.user.profile.is_restaurant_owner:
                from restaurants.models import Restaurant
                try:
                    donation.restaurant = Restaurant.objects.filter(owner=request.user).first()
                except:
                    pass
            
            donation.save()
            messages.success(request, '✅ Food donation created successfully! Thank you for reducing food waste.')
            return redirect('donations:my_donations')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form with user's phone if available
        initial = {}
        if hasattr(request.user, 'profile') and request.user.profile.phone:
            initial['phone'] = request.user.profile.phone
        form = DonationForm(initial=initial)
    
    context = {
        'form': form,
        'geoapify_api_key': 'e0f8bf51ccb649ea846a4ff8312d98cb',
    }
    return render(request, 'donations/donate_food.html', context)


@login_required
def book_donation(request, donation_id):
    """Book a donation for collection"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Check if donation is available
    if not donation.is_available:
        messages.error(request, 'This donation is no longer available.')
        return redirect('donations:donation_detail', donation_id)
    
    # Check if user is trying to book their own donation
    if donation.donor == request.user:
        messages.error(request, 'You cannot book your own donation.')
        return redirect('donations:donation_detail', donation_id)
    
    if request.method == 'POST':
        # Book the donation
        donation.is_booked = True
        donation.booked_by = request.user
        donation.booked_at = timezone.now()
        donation.status = 'booked'
        donation.save()
        
        # Create order entry for tracking
        from decimal import Decimal
        order = Order.objects.create(
            user=request.user,
            restaurant=donation.restaurant,
            total_amount=Decimal('0.00'),  # Free donation
            delivery_fee=Decimal('0.00'),
            tax_amount=Decimal('0.00'),
            status='confirmed',
            confirmed_at=timezone.now(),
            delivery_address=donation.address,
            payment_status='completed',
            is_paid=True,
            # Add donation location
            delivery_latitude=donation.latitude,
            delivery_longitude=donation.longitude,
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            name=f"Donation: {donation.food_name}",
            price=Decimal('0.00'),
            quantity=1,
        )
        
        # Create notification for donor
        Notification.objects.create(
            user=donation.donor,
            donation=donation,
            message=f"🎉 {request.user.username} has booked your donation: {donation.food_name}"
        )
        
        messages.success(request, 
            f'✅ Successfully booked {donation.food_name}! '
            f'Please collect from: {donation.address}. '
            f'Contact: {donation.phone}'
        )
        return redirect('donations:my_bookings')
    
    context = {
        'donation': donation,
        'geoapify_api_key': 'e0f8bf51ccb649ea846a4ff8312d98cb',
    }
    return render(request, 'donations/book_donation.html', context)


@login_required
def cancel_booking(request, donation_id):
    """Cancel a booked donation"""
    donation = get_object_or_404(Donation, id=donation_id, booked_by=request.user)
    
    if donation.status == 'booked':
        donation.is_booked = False
        donation.booked_by = None
        donation.booked_at = None
        donation.status = 'available'
        donation.save()
        
        # Notify donor
        Notification.objects.create(
            user=donation.donor,
            donation=donation,
            message=f"{request.user.username} cancelled their booking for: {donation.food_name}"
        )
        
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this donation.')
    
    return redirect('donations:my_bookings')


@login_required
def mark_as_collected(request, donation_id):
    """Mark donation as collected"""
    donation = get_object_or_404(Donation, id=donation_id, booked_by=request.user)
    
    if donation.status == 'booked':
        donation.status = 'collected'
        donation.save()
        
        # Notify donor
        Notification.objects.create(
            user=donation.donor,
            donation=donation,
            message=f"✅ {request.user.username} has collected: {donation.food_name}"
        )
        
        messages.success(request, '✅ Marked as collected. Thank you for helping reduce food waste!')
    else:
        messages.error(request, 'Cannot mark this donation as collected.')
    
    return redirect('donations:my_bookings')


@login_required
def my_donations(request):
    """View user's donated food items"""
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    
    context = {
        'donations': donations,
        'active_tab': 'my_donations',
    }
    return render(request, 'donations/my_donations.html', context)


@login_required
def my_bookings(request):
    """View user's booked donations"""
    bookings = Donation.objects.filter(booked_by=request.user).order_by('-booked_at')
    
    context = {
        'bookings': bookings,
        'active_tab': 'my_bookings',
    }
    return render(request, 'donations/my_bookings.html', context)


@login_required
def delete_donation(request, donation_id):
    """Delete a donation (only donor can delete)"""
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    
    if donation.is_booked:
        messages.error(request, 'Cannot delete a booked donation. Ask the user to cancel first.')
        return redirect('donations:my_donations')
    
    donation.delete()
    messages.success(request, 'Donation deleted successfully.')
    return redirect('donations:my_donations')


# For backward compatibility with old views
@login_required
def ngo_dashboard(request):
    """Redirect to my_bookings"""
    return redirect('donations:my_bookings')
