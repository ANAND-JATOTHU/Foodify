from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from orders.models import Order
from accounts.models import DeliveryAgent
import json


@login_required
def delivery_dashboard(request):
    """Enhanced delivery agent dashboard with live orders"""
    if not request.user.profile.is_delivery_agent:
        messages.error(request, 'Access denied. Delivery agents only.')
        return redirect('index')
    
    try:
        delivery_agent = request.user.delivery_profile
    except DeliveryAgent.DoesNotExist:
        messages.error(request, 'Delivery agent profile not found.')
        return redirect('index')
    
    # Filter orders by status for different tabs
    available_orders = Order.objects.filter(
        status='confirmed',
        delivery_agent=None
    ).order_by('-created_at')[:20]
    
    # Orders assigned to this agent
    assigned_orders = Order.objects.filter(delivery_agent=request.user)
    
    # Orders picked up and out for delivery
    active_orders = assigned_orders.filter(status='out_for_delivery').order_by('-picked_at')
    
    # Completed deliveries
    delivered_orders = assigned_orders.filter(status='delivered').order_by('-delivered_at')[:10]
    
    # Statistics
    total_deliveries = delivered_orders.count()
    pending_pickups = assigned_orders.filter(status__in=['confirmed', 'preparing']).count()
    
    context = {
        'delivery_agent': delivery_agent,
        'available_orders': available_orders,
        'pending_pickups': assigned_orders.filter(status__in=['confirmed', 'preparing']),
        'active_orders': active_orders,
        'delivered_orders': delivered_orders,
        'total_deliveries': delivery_agent.total_deliveries,
        'total_earnings': delivery_agent.total_earnings,
        'pending_pickups_count': pending_pickups,
    }
    
    return render(request, 'delivery/delivery_dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def accept_order(request, order_id):
    """Accept an available order and assign to current agent"""
    if not request.user.profile.is_delivery_agent:
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    order = get_object_or_404(Order, id=order_id)
    
    # Check if order is available
    if order.delivery_agent is not None:
        return JsonResponse({'success': False, 'error': 'Order already assigned'}, status=400)
    
    if order.status not in ['confirmed', 'preparing']:
        return JsonResponse({'success': False, 'error': 'Order not available for pickup'}, status=400)
    
    # Assign agent to order
    order.delivery_agent = request.user
    order.save()
    
    messages.success(request, f'Order #{order.id} accepted! Head to the restaurant to pick it up.')
    return JsonResponse({
        'success': True,
        'message': 'Order accepted successfully',
        'order_id': order.id
    })


@login_required
@require_http_methods(["POST"])
def mark_as_picked(request, order_id):
    """
    Mark order as picked up from restaurant.
    AUTO STATUS UPDATE: confirmed/preparing → out_for_delivery
    """
    if not request.user.profile.is_delivery_agent:
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    order = get_object_or_404(Order, id=order_id, delivery_agent=request.user)
    
    if order.status not in ['confirmed', 'preparing']:
        return JsonResponse({'success': False, 'error': 'Order cannot be picked up in current status'}, status=400)
    
    # AUTOMATIC STATUS UPDATE
    order.status = 'out_for_delivery'
    order.picked_at = timezone.now()
    
    # Copy restaurant location to order for tracking
    if order.restaurant:
        order.restaurant_latitude = order.restaurant.latitude
        order.restaurant_longitude = order.restaurant.longitude
    
    order.save()
    
    messages.success(request, f'Order #{order.id} marked as picked up! Navigate to customer location.')
    return JsonResponse({
        'success': True,
        'message': 'Order marked as picked up',
        'order_id': order.id,
        'status': order.status,
        'redirect_url': f'/delivery/route/{order.id}/'
    })


@login_required
@require_http_methods(["POST"])
def mark_as_delivered(request, order_id):
    """
    Mark order as delivered to customer.
    AUTO STATUS UPDATE: out_for_delivery → delivered
    """
    if not request.user.profile.is_delivery_agent:
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    order = get_object_or_404(Order, id=order_id, delivery_agent=request.user)
    
    if order.status != 'out_for_delivery':
        return JsonResponse({'success': False, 'error': 'Order not out for delivery'}, status=400)
    
    # AUTOMATIC STATUS UPDATE
    order.status = 'delivered'
    order.delivered_at = timezone.now()
    order.save()
    
    # Update agent statistics
    agent = request.user.delivery_profile
    agent.total_deliveries += 1
    agent.total_earnings += order.delivery_fee
    agent.save()
    
    messages.success(request, f'Order #{order.id} delivered successfully! Great job!')
    return JsonResponse({
        'success': True,
        'message': 'Order delivered successfully',
        'order_id': order.id,
        'status': order.status,
        'redirect_url': '/delivery/dashboard/'
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_agent_location(request):
    """
    Update agent's current location during delivery.
    Called periodically from mobile app/browser to share live location with customer.
    """
    if not request.user.profile.is_delivery_agent:
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        order_id = data.get('order_id')
        
        if not all([latitude, longitude, order_id]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
        
        # Get order being delivered
        order = Order.objects.get(
            id=order_id,
            delivery_agent=request.user,
            status='out_for_delivery'
        )
        
        # Update agent's live location
        order.agent_current_latitude = latitude
        order.agent_current_longitude = longitude
        order.agent_location_updated_at = timezone.now()
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Location updated',
            'timestamp': order.agent_location_updated_at.isoformat()
        })
        
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found or not assigned'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def route_map_view(request, order_id):
    """
    Display Google Maps route from restaurant to delivery location.
    Shows turn-by-turn navigation for delivery agent.
    """
    if not request.user.profile.is_delivery_agent:
        messages.error(request, 'Access denied.')
        return redirect('index')
    
    order = get_object_or_404(Order, id=order_id, delivery_agent=request.user)
    
    if order.status not in ['out_for_delivery']:
        messages.warning(request, 'This order is not currently out for delivery.')
    
    context = {
        'order': order,
        'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY',  # Will be added from settings
    }
    
    return render(request, 'delivery/route_map.html', context)


@login_required
def reject_order(request, order_id):
    """Reject an assigned order (remove assignment)"""
    if not request.user.profile.is_delivery_agent:
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    order = get_object_or_404(Order, id=order_id, delivery_agent=request.user)
    
    # Can only reject if not yet picked up
    if order.status in ['confirmed', 'preparing'] and not order.picked_at:
        order.delivery_agent = None
        order.save()
        messages.success(request, f'Order #{order.id} rejected.')
        return JsonResponse({'success': True, 'message': 'Order rejected'})
    else:
        return JsonResponse({'success': False, 'error': 'Cannot reject order after pickup'}, status=400)


@login_required
def toggle_availability(request):
    """Toggle delivery agent availability status"""
    if not request.user.profile.is_delivery_agent:
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    agent = request.user.delivery_profile
    agent.availability_status = not agent.availability_status
    agent.save()
    
    status_text = "available" if agent.availability_status else "unavailable"
    messages.success(request, f'You are now {status_text} for deliveries.')
    
    return JsonResponse({
        'success': True,
        'available': agent.availability_status,
        'message': f'Status changed to {status_text}'
    })
