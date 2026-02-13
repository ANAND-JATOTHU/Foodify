from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from orders.models import Order
from restaurants.models import Restaurant


class PaymentTransaction(models.Model):
    """
    Track all payment transactions with complete details.
    Linked to orders and restaurants for filtering and reporting.
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet'),
        ('cod', 'Cash on Delivery'),
    ]
    
    # Core relationships
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment_transaction',
        help_text='Associated order'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payment_transactions',
        help_text='Restaurant for this transaction (for owner filtering)'
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_transactions',
        help_text='Customer who made the payment'
    )
    
    # Payment details
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        help_text='Unique transaction ID from payment gateway'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='stripe'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Total transaction amount'
    )
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Gateway response data
    gateway_response = models.JSONField(
        blank=True,
        null=True,
        help_text='Payment gateway response data'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['restaurant', '-created_at']),
            models.Index(fields=['customer', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Transaction #{self.transaction_id} - Order #{self.order.id} - ₹{self.amount}"
    
    def mark_completed(self):
        """Mark transaction as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])
    
    def mark_failed(self):
        """Mark transaction as failed"""
        self.status = 'failed'
        self.save(update_fields=['status', 'updated_at'])


class PaymentNotification(models.Model):
    """
    In-app notifications for payment events.
    Sent to restaurant owners and customers.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('payment_success', 'Payment Successful'),
        ('payment_failed', 'Payment Failed'),
        ('order_confirmed', 'Order Confirmed'),
        ('refund_processed', 'Refund Processed'),
    ]
    
    # Relationships
    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_notifications'
    )
    
    # Notification details
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPE_CHOICES
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Notification'
        verbose_name_plural = 'Payment Notifications'
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
