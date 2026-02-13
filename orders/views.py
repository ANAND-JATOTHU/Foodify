from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import stripe
import json
from .models import Cart, Order, OrderItem, Payment
from restaurants.models import Restaurant, MenuItem
from payments import get_payment_model


@login_required
def add_to_cart(request, item_id):
    """Add menu item to cart"""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # Get or create cart item
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        menu_item=menu_item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{menu_item.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'restaurants:list'))


@login_required
def view_cart(request):
    """View shopping cart with recent orders"""
    from orders.models import Order
    
    cart_items = Cart.objects.filter(user=request.user).select_related('menu_item', 'menu_item__restaurant')
    
    # Get recent orders (last 5)
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calculate totals
    subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
    delivery_fee = Decimal('40.00') if cart_items.exists() else Decimal('0.00')
    tax = subtotal * Decimal('0.05')  # 5% tax
    total = subtotal + delivery_fee + tax
    
    context = {
        'cart_items': cart_items,
        'recent_orders': recent_orders,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                messages.success(request, 'Item removed from cart')
                return redirect('orders:view_cart')
        
        messages.success(request, 'Cart updated!')
    
    return redirect('orders:view_cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    item_name = cart_item.menu_item.name
    cart_item.delete()
    messages.success(request, f'{item_name} removed from cart')
    return redirect('orders:view_cart')


@login_required
def clear_cart(request):
    """Clear entire cart"""
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Cart cleared!')
    return redirect('orders:view_cart')


@login_required
def place_order(request):
    """Redirect to checkout page"""
    cart_items = Cart.objects.filter(user=request.user).select_related('menu_item', 'menu_item__restaurant')
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('orders:view_cart')
    
    if request.method == 'POST':
        # Get delivery details
        delivery_address = request.POST.get('delivery_address', request.user.profile.address or '')
        phone = request.POST.get('phone', request.user.profile.phone or '')
        
        if not delivery_address or not phone:
            messages.error(request, 'Please provide delivery address and phone number')
            return redirect('orders:view_cart')
        
        # Store delivery info in session
        request.session['delivery_address'] = delivery_address
        request.session['phone'] = phone
        
        # Redirect to checkout
        return redirect('orders:checkout')
    
    return redirect('orders:view_cart')


@login_required
def order_history(request):
    """View user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all().select_related('menu_item', 'menu_item__restaurant')
    
    # Calculate grand total from components
    grand_total = order.total_amount + order.delivery_fee + order.tax_amount
    
    context = {
        'order': order,
        'order_items': order_items,
        'grand_total': grand_total,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def track_order(request, order_id):
    """Live order tracking with delivery agent location"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all().select_related('menu_item')
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/track_order.html', context)


@login_required
def get_agent_location(request, order_id):
    """API endpoint to get delivery agent's current location"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'out_for_delivery' or not order.agent_current_latitude:
        return JsonResponse({'latitude': None, 'longitude': None})
    
    return JsonResponse({
        'latitude': str(order.agent_current_latitude),
        'longitude': str(order.agent_current_longitude),
        'updated_at': order.agent_location_updated_at.isoformat() if order.agent_location_updated_at else None
    })


# RESTAURANT OWNER VIEWS
@login_required
def owner_orders(request):
    """Restaurant owner order management"""
    if not request.user.profile.is_restaurant_owner:
        messages.error(request, 'Access denied. This page is for restaurant owners only.')
        return redirect('accounts:user_home')
    
    # Get all restaurants owned by this user
    restaurants = Restaurant.objects.filter(owner=request.user)
    
    # Get all orders for these restaurants
    orders = Order.objects.filter(restaurant__in=restaurants).select_related('user', 'restaurant').prefetch_related('items').order_by('-created_at')
    
    context = {
        'orders': orders,
        'restaurants': restaurants,
    }
    return render(request, 'orders/owner_orders.html', context)


@login_required
def update_order_status(request, order_id):
    """Update order status by restaurant owner"""
    order = get_object_or_404(Order, id=order_id, restaurant__owner=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('orders:owner_orders')


@login_required
def owner_order_detail(request, order_id):
    """View order details for restaurant owner"""
    # Verify user is a restaurant owner
    if not request.user.profile.is_restaurant_owner:
        messages.error(request, 'Access denied. This page is for restaurant owners only.')
        return redirect('accounts:user_home')
    
    # Get the order and verify it belongs to one of the user's restaurants
    order = get_object_or_404(Order, id=order_id, restaurant__owner=request.user)
    order_items = order.items.all().select_related('menu_item')
    
    # Calculate grand total from components
    grand_total = order.total_amount + order.delivery_fee + order.tax_amount
    
    context = {
        'order': order,
        'order_items': order_items,
        'grand_total': grand_total,
        'STATUS_CHOICES': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/owner_order_detail.html', context)


# PAYMENT VIEWS - Django-Payments
@login_required
def checkout(request):
    """Stripe Payment Element checkout page"""
    cart_items = Cart.objects.filter(user=request.user).select_related('menu_item', 'menu_item__restaurant')
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('orders:view_cart')
    
    # Get delivery info from session
    delivery_address = request.session.get('delivery_address', '')
    phone = request.session.get('phone', '')
    
    if not delivery_address or not phone:
        messages.error(request, 'Please provide delivery details first')
        return redirect('orders:view_cart')
    
    # Calculate totals
    subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
    delivery_fee = Decimal('40.00')
    tax = subtotal * Decimal('0.05')
    grand_total = subtotal + delivery_fee + tax
    
    # Store cart info in session for payment confirmation
    request.session['checkout_amount'] = str(grand_total)
    request.session['checkout_subtotal'] = str(subtotal)
    request.session['checkout_delivery_fee'] = str(delivery_fee)
    request.session['checkout_tax'] = str(tax)
    
    # Pass Stripe public key to template
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'grand_total': grand_total,
        'delivery_address': delivery_address,
        'phone': phone,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def payment_success(request):
    """Handle successful payment"""
    import uuid
    from django.conf import settings
    from payment_system.models import PaymentTransaction
    
    payment_id = request.GET.get('payment_id')
    
    if not payment_id:
        messages.error(request, 'Invalid payment session')
        return redirect('orders:view_cart')
    
    try:
        # Get the payment object
        payment = Payment.objects.get(id=payment_id)
        
        # Check if payment already processed
        if hasattr(payment, 'order') and payment.order:
            return render(request, 'orders/payment_success.html', {
                'order': payment.order,
                'grand_total': payment.total,
            })
        
        # Get cart items
        cart_items = Cart.objects.filter(user=request.user).select_related('menu_item', 'menu_item__restaurant')
        
        if not cart_items.exists():
            messages.error(request, 'Cart is empty')
            return redirect('orders:view_cart')
        
        # Get delivery info from session
        delivery_address = request.session.get('delivery_address', '')
        phone = request.session.get('phone', '')
        
        # Calculate totals
        subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
        delivery_fee = Decimal('40.00')
        tax = subtotal * Decimal('0.05')
        grand_total = subtotal + delivery_fee + tax
        
        from django.utils import timezone
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            restaurant=cart_items.first().menu_item.restaurant,
            total_amount=subtotal,
            delivery_fee=delivery_fee,
            tax_amount=tax,
            status='confirmed',  # Auto-confirm paid orders
            confirmed_at=timezone.now(),  # AUTO TIMESTAMP: payment → confirmed
            delivery_address=f"{delivery_address}\nPhone: {phone}",
            payment_status='completed',
            is_paid=True,
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                name=cart_item.menu_item.name,
                price=cart_item.menu_item.price,
                quantity=cart_item.quantity
            )
        
        # Link payment to order
        payment.order = order
        payment.save()
        
        # Create payment transaction record
        transaction = PaymentTransaction.objects.create(
            order=order,
            restaurant=order.restaurant,
            customer=request.user,
            transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            payment_method='stripe',
            amount=grand_total,
            currency='INR',
            status='completed',
            gateway_response={'payment_id': payment_id}
        )
        transaction.mark_completed()
        
        # Notifications will be automatically sent via signals
        
        # Clear cart
        cart_items.delete()
        
        # Clear session
        request.session.pop('delivery_address', None)
        request.session.pop('phone', None)
        request.session.pop('pending_payment_id', None)
        
        return render(request, 'orders/payment_success.html', {
            'order': order,
            'grand_total': grand_total,
            'transaction': transaction,
        })
    
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found')
        return redirect('orders:view_cart')
    except Exception as e:
        messages.error(request, f'Error creating order: {str(e)}')
        return redirect('orders:view_cart')



@login_required
def payment_cancel(request):
    """Handle cancelled/failed payment"""
    messages.warning(request, 'Payment was cancelled. Your cart items are still saved.')
    return redirect('orders:view_cart')


# STRIPE PAYMENT ELEMENT API
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@require_POST
def create_payment_intent(request):
    """Create a Stripe Payment Intent for checkout"""
    try:
        # Get amount from session
        amount_str = request.session.get('checkout_amount')
        if not amount_str:
            return JsonResponse({'error': 'No checkout session found'}, status=400)
        
        amount = Decimal(amount_str)
        # Convert to smallest currency unit (paise for INR)
        amount_cents = int(amount * 100)
        
        # Create Payment Intent with automatic payment methods
        # This enables all payment methods available in your Stripe account (cards, UPI, wallets, etc.)
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='inr',
            automatic_payment_methods={'enabled': True},  # Enable all available payment methods
            metadata={
                'user_id': str(request.user.id),
                'username': request.user.username,
            }
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'paymentIntentId': intent.id
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_POST
def confirm_payment(request):
    """Confirm payment and create order"""
    try:
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')
        
        if not payment_intent_id:
            return JsonResponse({'error': 'Payment Intent ID required'}, status=400)
        
        # Verify Payment Intent with Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status != 'succeeded':
            return JsonResponse({'error': 'Payment not successful'}, status=400)
        
        # Get cart and session data
        cart_items = Cart.objects.filter(user=request.user).select_related('menu_item', 'menu_item__restaurant')
        
        if not cart_items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Get delivery info from session
        delivery_address = request.session.get('delivery_address', '')
        subtotal = Decimal(request.session.get('checkout_subtotal', '0'))
        delivery_fee = Decimal(request.session.get('checkout_delivery_fee', '0'))
        tax = Decimal(request.session.get('checkout_tax', '0'))
        grand_total = Decimal(request.session.get('checkout_amount', '0'))
        
        from payment_system.models import PaymentTransaction
        
        # Get restaurant
        restaurant = cart_items.first().menu_item.restaurant
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
            status='confirmed',
            confirmed_at=timezone.now(),  # AUTO TIMESTAMP: payment → confirmed
            delivery_address=delivery_address,
            total_amount=subtotal,
            delivery_fee=delivery_fee,
            tax_amount=tax,
            payment_status='paid',
            payment_intent_id=payment_intent_id,
            is_paid=True
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                name=cart_item.menu_item.name,
                price=cart_item.menu_item.price,
                quantity=cart_item.quantity
            )
        
        # Determine payment method
        payment_method_type = 'card'  # Default
        if hasattr(intent, 'payment_method') and intent.payment_method:
            pm = stripe.PaymentMethod.retrieve(intent.payment_method)
            payment_method_type = pm.type
        
        # Create payment transaction
        PaymentTransaction.objects.create(
            order=order,
            restaurant=restaurant,
            customer=request.user,
            transaction_id=payment_intent_id,
            payment_method=payment_method_type,
            amount=grand_total,
            currency='INR',
            status='completed',
            gateway_response={
                'payment_intent_id': payment_intent_id,
                'status': intent.status,
                'payment_method_type': payment_method_type
            }
        )
        
        # Clear cart
        cart_items.delete()
        
        # Clear session
        request.session.pop('delivery_address', None)
        request.session.pop('phone', None)
        request.session.pop('checkout_amount', None)
        request.session.pop('checkout_subtotal', None)
        request.session.pop('checkout_delivery_fee', None)
        request.session.pop('checkout_tax', None)
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'redirect_url': f'/orders/{order.id}/'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
