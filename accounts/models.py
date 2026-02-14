from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('delivery_agent', 'Delivery Agent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile ({self.get_user_type_display()})"
    
    @property
    def is_customer(self):
        return self.user_type == 'customer'
    
    @property
    def is_restaurant_owner(self):
        return self.user_type == 'restaurant_owner'
    
    @property
    def is_delivery_agent(self):
        return self.user_type == 'delivery_agent'
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class DeliveryAgent(models.Model):
    """Delivery agent profile with vehicle and license information"""
    VEHICLE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('scooter', 'Scooter'),
        ('cycle', 'Cycle'),
        ('car', 'Car'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_profile')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    vehicle_number = models.CharField(max_length=20)
    driving_license = models.CharField(max_length=50)
    availability_status = models.BooleanField(default=True)
    id_proof = models.FileField(upload_to='delivery_agents/id_proofs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.user.username}"
    
    @property
    def total_deliveries(self):
        """Count of delivered orders"""
        return self.user.assigned_orders.filter(status='delivered').count()
    
    @property
    def total_earnings(self):
        """Total earnings from delivered orders"""
        from decimal import Decimal
        delivered_orders = self.user.assigned_orders.filter(status='delivered')
        return sum(order.delivery_fee for order in delivered_orders) or Decimal('0.00')
    
    class Meta:
        verbose_name = 'Delivery Agent'
        verbose_name_plural = 'Delivery Agents'



# Signal to auto-create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
