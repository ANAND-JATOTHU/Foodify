from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Donation(models.Model):
    """Enhanced donation model with quantity tracking, expiry, and multi-user booking support"""
    CATEGORY_CHOICES = [
        ('cooked', 'Cooked Food'),
        ('raw', 'Raw Materials'),
        ('packaged', 'Packaged Food'),
        ('baked', 'Baked Goods'),
        ('other', 'Other'),
    ]
    
    FOOD_TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('partially_booked', 'Partially Booked'),
        ('fully_booked', 'Fully Booked'),
        ('collected', 'Collected'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    QUANTITY_UNIT_CHOICES = [
        ('servings', 'Servings'),
        ('kg', 'Kilograms'),
        ('pieces', 'Pieces'),
        ('plates', 'Plates'),
        ('packets', 'Packets'),
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
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES, default='veg')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='cooked')
    description = models.TextField(blank=True, help_text='Additional details about the food')
    image = models.ImageField(upload_to='donation_images/', blank=True, null=True, help_text='Image of the food item')
    
    # Quantity Management (NEW)
    original_quantity = models.IntegerField(help_text='Total quantity available initially')
    available_quantity = models.IntegerField(help_text='Quantity still available for booking')
    quantity_unit = models.CharField(max_length=20, choices=QUANTITY_UNIT_CHOICES, default='servings')
    
    # Legacy quantity fields (kept for backward compatibility)
    quantity_description = models.CharField(max_length=100, blank=True, help_text="e.g., 5 kg, 10 plates")
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
        help_text='Number of people this can serve (deprecated - use original_quantity)'
    )
    
    # Time Management (ENHANCED)
    prepared_time = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='When the food was prepared'
    )
    expiry_time = models.DateTimeField(
        help_text='When the food expires and should be removed from listings'
    )
    best_before = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Recommended consumption time'
    )
    
    # Location Details
    location = models.CharField(max_length=500, help_text='Pickup location address')
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text='Latitude for map location'
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text='Longitude for map location'
    )
    
    # Contact Information
    contact_phone = models.CharField(max_length=15, help_text='Contact number for pickup')
    contact_name = models.CharField(max_length=100, blank=True, help_text='Contact person name')
    
    # Booking Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Info
    pickup_instructions = models.TextField(blank=True, help_text='Special instructions for pickup')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'expiry_time']),
            models.Index(fields=['donor']),
        ]
    
    def __str__(self):
        return f"{self.food_name} by {self.donor.username}"
    
    @property
    def is_available(self):
        """Check if donation is available for booking"""
        return (
            self.status in ['available', 'partially_booked'] and
            self.available_quantity > 0 and
            not self.is_expired
        )
    
    @property
    def is_expired(self):
        """Check if donation has expired"""
        return timezone.now() > self.expiry_time
    
    @property
    def time_remaining(self):
        """Get time remaining until expiry"""
        if self.is_expired:
            return None
        return self.expiry_time - timezone.now()
    
    @property
    def hours_until_expiry(self):
        """Get hours remaining until expiry"""
        if self.is_expired:
            return 0
        delta = self.time_remaining
        return delta.total_seconds() / 3600
    
    @property
    def urgency_level(self):
        """Get urgency level based on time remaining"""
        hours = self.hours_until_expiry
        if hours <= 0:
            return 'expired'
        elif hours <= 2:
            return 'critical'
        elif hours <= 6:
            return 'high'
        elif hours <= 12:
            return 'medium'
        else:
            return 'low'
    
    @property
    def quantity_booked(self):
        """Get total quantity booked"""
        return self.original_quantity - self.available_quantity
    
    @property
    def booking_percentage(self):
        """Get percentage of quantity booked"""
        if self.original_quantity == 0:
            return 0
        return (self.quantity_booked / self.original_quantity) * 100
    
    def update_status(self):
        """Update donation status based on available quantity"""
        if self.is_expired:
            self.status = 'expired'
        elif self.available_quantity == 0:
            self.status = 'fully_booked'
        elif self.available_quantity < self.original_quantity:
            self.status = 'partially_booked'
        else:
            self.status = 'available'
        self.save()


class DonationBooking(models.Model):
    """Track individual bookings of donations with quantities"""
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('collected', 'Collected'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    # Relationships
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='bookings')
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_bookings')
    
    # Booking Details
    quantity_booked = models.IntegerField(help_text='Quantity booked from this donation')
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='confirmed')
    
    # Booker Information
    booker_name = models.CharField(max_length=100, help_text='Name of person collecting')
    booker_phone = models.CharField(max_length=15, help_text='Contact number')
    booker_email = models.EmailField(blank=True, help_text='Email for notifications')
    
    # Collection Details
    preferred_collection_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When booker plans to collect'
    )
    actual_collection_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When actually collected'
    )
    
    # Additional Info
    notes = models.TextField(blank=True, help_text='Special requests or notes')
    
    # Timestamps
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Rating (optional)
    rating = models.IntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text='Rating by booker (1-5)'
    )
    feedback = models.TextField(blank=True, help_text='Feedback from booker')
    
    class Meta:
        ordering = ['-booked_at']
        indexes = [
            models.Index(fields=['donation', 'booking_status']),
            models.Index(fields=['booked_by']),
        ]
    
    def __str__(self):
        return f"{self.booker_name} booked {self.quantity_booked} {self.donation.quantity_unit} of {self.donation.food_name}"
    
    @property
    def is_active(self):
        """Check if booking is still active"""
        return self.booking_status in ['pending', 'confirmed']
    
    def cancel(self):
        """Cancel this booking and restore quantity to donation"""
        if self.is_active:
            self.booking_status = 'cancelled'
            self.save()
            
            # Restore quantity to donation
            self.donation.available_quantity += self.quantity_booked
            self.donation.update_status()
            return True
        return False
    
    def mark_collected(self):
        """Mark booking as collected"""
        self.booking_status = 'collected'
        self.actual_collection_time = timezone.now()
        self.save()
        
        # Check if all bookings are collected
        all_collected = not self.donation.bookings.filter(booking_status__in=['pending', 'confirmed']).exists()
        if all_collected and self.donation.available_quantity == 0:
            self.donation.status = 'collected'
            self.donation.save()



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
