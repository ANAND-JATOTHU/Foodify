from django import forms
from .models import Donation, DonationProof
from django.utils import timezone


class DonationForm(forms.ModelForm):
    """Form for creating/editing food donations"""
    
    class Meta:
        model = Donation
        fields = [
            'food_name', 'food_type', 'category', 'description', 'image',
            'quantity_description', 'weight_kg', 'serving_count',
            'address', 'latitude', 'longitude',
            'phone', 'pickup_instructions',
            'prepared_time', 'expiry_time', 'available_until'
        ]
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Vegetable Biryani'}),
            'food_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional details about the food...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            
            'quantity_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 kg, 20 plates, 10 servings'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Approximate weight in kg', 'step': '0.1'}),
            'serving_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of people it can serve'}),
            
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Pickup address'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'}),
            'pickup_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any special instructions for pickup...'}),
            
            'prepared_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'expiry_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'available_until': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) != 10:
            raise forms.ValidationError('Phone number must be 10 digits')
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        expiry_time = cleaned_data.get('expiry_time')
        
        # Auto-set expiry_time if not provided (2 hours from now for cooked food)
        if not expiry_time and cleaned_data.get('category') == 'cooked':
            cleaned_data['expiry_time'] = timezone.now() + timezone.timedelta(hours=2)
        
        return cleaned_data


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
