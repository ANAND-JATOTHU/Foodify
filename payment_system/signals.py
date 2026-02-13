from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .models import PaymentTransaction, PaymentNotification


@receiver(post_save, sender=Order)
def create_payment_notification(sender, instance, created, **kwargs):
    """
    Automatically send notifications when order is confirmed after payment.
    """
    # Only process if order is paid and confirmed
    if not instance.is_paid or instance.status != 'confirmed':
        return
    
    # Check if payment transaction exists
    if not hasattr(instance, 'payment_transaction'):
        return
    
    transaction = instance.payment_transaction
    
    # Check if notifications already sent (to avoid duplicates)
    if transaction.notifications.exists():
        return
    
    # Send notification to restaurant owner
    if instance.restaurant and instance.restaurant.owner:
        owner_notification = PaymentNotification.objects.create(
            transaction=transaction,
            recipient=instance.restaurant.owner,
            notification_type='payment_success',
            title=f'New Order Received - #{instance.id}',
            message=f'You received a new order (Order ID: #{instance.id}) worth ₹{instance.grand_total}. '
                    f'Payment completed successfully. Please prepare the order.\n'
                    f'Customer: {instance.user.get_full_name() or instance.user.username}\n'
                    f'Items: {instance.items.count()} items'
        )
    
    # Send confirmation to customer
    customer_notification = PaymentNotification.objects.create(
        transaction=transaction,
        recipient=instance.user,
        notification_type='order_confirmed',
        title=f'Order Confirmed - #{instance.id}',
        message=f'Your order has been confirmed! Order ID: #{instance.id}\n'
                f'Restaurant: {instance.restaurant.name if instance.restaurant else "N/A"}\n'
                f'Total Amount: ₹{instance.grand_total}\n'
                f'Your order is being prepared and will be delivered soon.'
    )


@receiver(post_save, sender=PaymentTransaction)
def update_transaction_status(sender, instance, created, **kwargs):
    """
    Handle payment transaction status changes.
    """
    if created:
        return
    
    # If payment failed, send notification
    if instance.status == 'failed':
        # Check if failure notification already exists
        if not instance.notifications.filter(notification_type='payment_failed').exists():
            PaymentNotification.objects.create(
                transaction=instance,
                recipient=instance.customer,
                notification_type='payment_failed',
                title='Payment Failed',
                message=f'Your payment for Order #{instance.order.id} failed. '
                        f'Please try again or contact support.'
            )
