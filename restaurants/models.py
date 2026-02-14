from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurant(models.Model):
    """Restaurant model with all details"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_restaurants')
    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=100)
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=4.0
    )
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Restaurant latitude for maps')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Restaurant longitude for maps')
    distance = models.DecimalField(max_digits=4, decimal_places=1, default=5.0)  # in km
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    description = models.TextField()
    is_veg = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)  # Admin can approve/reject
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-rating']
        

class MenuItem(models.Model):
    """Menu items for restaurants"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    calories = models.PositiveIntegerField(blank=True, null=True, help_text='Calories per serving')
    is_available = models.BooleanField(default=True)
    is_veg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    
    class Meta:
        ordering = ['name']


class Favorite(models.Model):
    """User's favorite restaurants"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'restaurant')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"
