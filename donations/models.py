from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Donation(models.Model):
    """Enhanced donation model with location, booking, and detailed quantity tracking"""
    CATEGORY_CHOICES = [
        ('cooked', 'Cooked Food'),
        ('raw', 'Raw Materials'),
        ('packaged', 'Packaged Food'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('collected', 'Collected'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    # Donor Information
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    restaurant = models.ForeignKey(
        'restaurants.Restaurant', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='donations',
        help_text='If donated by a restaurant'
    )
    
    # Food Details
    food_name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=20, choices=[('veg', 'Veg'), ('non-veg', 'Non-Veg')], default='veg')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='cooked')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='donation_images/', blank=True, null=True, help_text='Image of the food item')
    
    # Quantity Details
    quantity_description = models.CharField(max_length=100, help_text="e.g., 5 kg, 10 plates")
    weight_kg = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Approximate weight in kilograms'
    )
    serving_count = models.IntegerField(
        null=True, 
        blank=True,
        help_text='Number of people this can serve'
    )
    
    # Location Information  
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Pickup location latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Pickup location longitude')
    
    # Contact Details
    phone = models.CharField(max_length=15)
    pickup_instructions = models.TextField(blank=True, help_text='Special instructions for pickup')
    
    # Timing
    prepared_time = models.DateTimeField(null=True, blank=True, help_text='When the food was prepared')
    expiry_time = models.DateTimeField(null=True, blank=True, help_text="Estimated time before food spoils")
    available_until = models.DateTimeField(null=True, blank=True, help_text='Available for pickup until')
    
    # Booking Information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='booked_donations',
        help_text='User who booked this donation'
    )
    booked_at = models.DateTimeField(null=True, blank=True, help_text='When the donation was booked')
    collection_time = models.DateTimeField(null=True, blank=True, help_text='Scheduled pickup time')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.food_name} - {self.donor.username}"
    
    @property
    def is_expired(self):
        """Check if donation has expired"""
        if self.expiry_time:
            return timezone.now() > self.expiry_time
        return False
    
    @property
    def is_available(self):
        """Check if donation is available for booking"""
        return self.status == 'available' and not self.is_booked and not self.is_expired

    class Meta:
        ordering = ['-created_at']


class DonationProof(models.Model):
    """Proof/images of completed donations"""
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='proof')
    image = models.ImageField(upload_to='donation_proofs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Proof for {self.donation.food_name}"


class Notification(models.Model):
    """Notifications for donation-related activities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"
    
    class Meta:
        ordering = ['-created_at']
