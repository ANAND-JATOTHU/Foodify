from django import forms
from .models import Donation, DonationProof, DonationBooking
from django.utils import timezone
from datetime import timedelta


class DonationForm(forms.ModelForm):
    """Enhanced form for creating donations with quantity and expiry"""
    
    class Meta:
        model = Donation
        fields = [
            'food_name', 'food_type', 'category', 'description', 'image',
            'original_quantity', 'quantity_unit',
            'location', 'latitude', 'longitude',
            'contact_phone', 'contact_name',
            'expiry_time', 'prepared_time',
            'pickup_instructions', 'tags'
        ]
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Biryani, Samosas'}),
            'food_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the food item'}),
            'original_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'e.g., 20'}),
            'quantity_unit': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'id': 'donation-location', 'placeholder': 'Enter pickup address'}),
            'latitude': forms.HiddenInput(attrs={'id': 'donation-latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'donation-longitude'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'expiry_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'prepared_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'pickup_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any special instructions'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., spicy, gluten-free'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        original_quantity = cleaned_data.get('original_quantity')
        expiry_time = cleaned_data.get('expiry_time')
        
        # Validate quantity
        if original_quantity and original_quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        
        # Validate expiry time is in the future
        if expiry_time and expiry_time <= timezone.now():
            raise forms.ValidationError("Expiry time must be in the future")
        
        return cleaned_data
    
    def save(self, commit=True):
        donation = super().save(commit=False)
        # Set available_quantity same as original_quantity when creating
        if not donation.pk:
            donation.available_quantity = donation.original_quantity
        if commit:
            donation.save()
        return donation


class DonationBookingForm(forms.ModelForm):
    """Form for booking a donation with quantity selection"""
    
    class Meta:
        model = DonationBooking
        fields = ['quantity_booked', 'booker_name', 'booker_phone', 'booker_email', 'preferred_collection_time', 'notes']
        widgets = {
            'quantity_booked': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'id': 'quantity-selector'}),
            'booker_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'booker_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'booker_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'preferred_collection_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any special requests'}),
        }
    
    def __init__(self, *args, donation=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.donation = donation
        self.user = user
        
        if donation:
            # Set max quantity to available
            self.fields['quantity_booked'].widget.attrs['max'] = donation.available_quantity
            self.fields['quantity_booked'].help_text = f'Available: {donation.available_quantity} {donation.quantity_unit}'
        
        if user and hasattr(user, 'profile'):
            # Pre-fill with user info
            self.fields['booker_name'].initial = user.get_full_name() or user.username
            self.fields['booker_phone'].initial = user.profile.phone if user.profile.phone else ''
            self.fields['booker_email'].initial = user.email
    
    def clean_quantity_booked(self):
        quantity = self.cleaned_data['quantity_booked']
        if self.donation and quantity > self.donation.available_quantity:
            raise forms.ValidationError(f'Only {self.donation.available_quantity} {self.donation.quantity_unit} available')
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1')
        return quantity


class DonationProofForm(forms.ModelForm):
    """Form for uploading proof of donation collection"""
    
    class Meta:
        model = DonationProof
        fields = ['image', 'notes']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any notes about the collection...'}),
        }


class DonationSearchForm(forms.Form):
    """Form for searching/filtering donations"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search food items...'
        })
    )
    
    food_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types'), ('veg', 'Vegetarian'), ('non-veg', 'Non-Vegetarian')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Donation.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    min_serving = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum servings'
        })
    )
