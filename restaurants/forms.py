from django import forms
from .models import Restaurant, MenuItem


class RestaurantForm(forms.ModelForm):
    """Form for restaurant owners to add/edit their restaurant"""
    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine', 'location', 'distance', 'image', 'description', 'is_veg']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cuisine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Italian, Chinese, Indian'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
        labels = {
            'is_veg': 'Pure Vegetarian Restaurant',
        }


class MenuItemForm(forms.ModelForm):
    """Form for restaurant owners to add/edit menu items"""
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'image', 'calories', 'is_veg', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 350'}),
        }
        labels = {
            'calories': 'Calories (per serving)',
            'is_veg': 'Vegetarian Item',
            'is_available': 'Currently Available',
        }
