from django.db import models
from django.contrib.auth.models import User
from restaurants.models import MenuItem, Restaurant


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'menu_item')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        return self.quantity * self.menu_item.price


class Order(models.Model):
    """Orders placed by users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    delivery_agent = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_orders',
        help_text='Delivery agent assigned to this order'
    )
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=40.00)
    tax_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField()
    
    # Location tracking fields
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Customer delivery location latitude')
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Customer delivery location longitude')
    restaurant_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Restaurant location latitude')
    restaurant_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Restaurant location longitude')
    
    # Agent live location (updated periodically during delivery)
    agent_current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Delivery agent current latitude')
    agent_current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Delivery agent current longitude')
    agent_location_updated_at = models.DateTimeField(null=True, blank=True, help_text='Last time agent location was updated')
    
    # Timestamps for delivery lifecycle
    confirmed_at = models.DateTimeField(null=True, blank=True, help_text='When order was confirmed after payment')
    picked_at = models.DateTimeField(null=True, blank=True, help_text='When agent picked up order from restaurant')
    delivered_at = models.DateTimeField(null=True, blank=True, help_text='When order was delivered to customer')
    
    # Payment fields
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    @property
    def grand_total(self):
        return self.total_amount + self.delivery_fee + self.tax_amount


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)  # Store name in case menu item is deleted
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        return self.quantity * self.price


from payments.models import BasePayment


class Payment(BasePayment):
    """Payment transaction records using django-payments"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
    
    def get_failure_url(self):
        return f'http://localhost:8000/orders/payment/cancel/'
    
    def get_success_url(self):
        return f'http://localhost:8000/orders/payment/success/?payment_id={self.pk}'
    
    def get_purchased_items(self):
        if self.order:
            return [{'name': item.name, 'quantity': item.quantity, 'price': str(item.price)} 
                    for item in self.order.items.all()]
        return []
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        if self.order:
            return f"Payment for Order #{self.order.id} - ₹{self.total}"
        return f"Payment #{self.pk} - ₹{self.total}"


