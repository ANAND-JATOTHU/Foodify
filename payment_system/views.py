from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate
from decimal import Decimal
from .models import PaymentTransaction, PaymentNotification
from restaurants.models import Restaurant
from datetime import datetime, timedelta


@login_required
def payment_history(request):
    """Customer payment history page"""
    # Get all payments for the current user
    transactions = PaymentTransaction.objects.filter(
        customer=request.user
    ).select_related('order', 'restaurant').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    # Search by order ID or transaction ID
    search_query = request.GET.get('search')
    if search_query:
        transactions = transactions.filter(
            Q(transaction_id__icontains=search_query) |
            Q(order__id__icontains=search_query)
        )
    
    context = {
        'transactions': transactions,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': PaymentTransaction.PAYMENT_STATUS_CHOICES,
    }
    return render(request, 'payments/payment_history.html', context)


@login_required
def owner_payment_dashboard(request):
    """Restaurant owner payment dashboard with analytics"""
    # Verify user is a restaurant owner
    if not request.user.profile.is_restaurant_owner:
        messages.error(request, 'Access denied. This page is for restaurant owners only.')
        return redirect('accounts:user_home')
    
    # Get all restaurants owned by this user
    restaurants = Restaurant.objects.filter(owner=request.user)
    
    # Filter by specific restaurant if requested
    restaurant_filter = request.GET.get('restaurant')
    selected_restaurant = None
    if restaurant_filter:
        try:
            selected_restaurant = restaurants.get(id=restaurant_filter)
            filtered_restaurants = [selected_restaurant]
        except Restaurant.DoesNotExist:
            filtered_restaurants = restaurants
    else:
        filtered_restaurants = restaurants
    
    # Get all payment transactions for owner's restaurants
    transactions = PaymentTransaction.objects.filter(
        restaurant__in=filtered_restaurants
    ).select_related('order', 'customer', 'restaurant').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    # Date range filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        transactions = transactions.filter(created_at__gte=date_from)
    if date_to:
        transactions = transactions.filter(created_at__lte=date_to)
    
    # Calculate analytics
    total_revenue = transactions.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    total_transactions = transactions.filter(status='completed').count()
    pending_payments = transactions.filter(status='pending').count()
    failed_payments = transactions.filter(status='failed').count()
    
    # Get recent transactions (last 20)
    recent_transactions = transactions[:20]
    
    # Get unread notifications
    unread_notifications = PaymentNotification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    # Daily revenue chart data (last 7 days)
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    daily_revenue = transactions.filter(
        status='completed',
        created_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        revenue=Sum('amount'),
        count=Count('id')
    ).order_by('date')
    
    context = {
        'restaurants': restaurants,
        'selected_restaurant': selected_restaurant,
        'transactions': recent_transactions,
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'pending_payments': pending_payments,
        'failed_payments': failed_payments,
        'unread_notifications': unread_notifications,
        'daily_revenue': list(daily_revenue),
        'status_filter': status_filter,
        'status_choices': PaymentTransaction.PAYMENT_STATUS_CHOICES,
    }
    return render(request, 'payments/owner_payment_dashboard.html', context)


@login_required
def payment_detail(request, transaction_id):
    """Detailed view of a specific payment transaction"""
    transaction = get_object_or_404(PaymentTransaction, id=transaction_id)
    
    # Check permissions
    is_owner = (
        request.user.profile.is_restaurant_owner and
        transaction.restaurant and
        transaction.restaurant.owner == request.user
    )
    is_customer = transaction.customer == request.user
    
    if not (is_owner or is_customer):
        messages.error(request, 'You do not have permission to view this transaction.')
        return redirect('accounts:user_home')
    
    context = {
        'transaction': transaction,
        'order': transaction.order,
        'order_items': transaction.order.items.all(),
        'is_owner': is_owner,
    }
    return render(request, 'payments/payment_detail.html', context)


@login_required
def notifications(request):
    """View all payment notifications"""
    user_notifications = PaymentNotification.objects.filter(
        recipient=request.user
    ).select_related('transaction', 'transaction__order').order_by('-created_at')
    
    # Filter by type if requested
    type_filter = request.GET.get('type')
    if type_filter:
        user_notifications = user_notifications.filter(notification_type=type_filter)
    
    # Separate read and unread
    unread = user_notifications.filter(is_read=False)
    read = user_notifications.filter(is_read=True)
    
    context = {
        'unread_notifications': unread,
        'read_notifications': read,
        'type_filter': type_filter,
        'notification_types': PaymentNotification.NOTIFICATION_TYPE_CHOICES,
    }
    return render(request, 'payments/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(
        PaymentNotification,
        id=notification_id,
        recipient=request.user
    )
    notification.mark_as_read()
    
    # Redirect back to where the user came from
    return redirect(request.META.get('HTTP_REFERER', 'payments:notifications'))


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    PaymentNotification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)
    
    messages.success(request, 'All notifications marked as read.')
    return redirect('payments:notifications')
