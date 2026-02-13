from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, DeliveryAgent
from django.core.exceptions import ValidationError
import re


class UserRegistrationForm(UserCreationForm):
    """Extended user creation form with additional fields"""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        required=True,
        widget=forms.RadioSelect,
        initial='customer'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'user_type']
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update profile with phone and user_type
            user.profile.user_type = self.cleaned_data['user_type']
            if self.cleaned_data.get('phone'):
                user.profile.phone = self.cleaned_data['phone']
            user.profile.save()
        return user


class DeliveryAgentRegistrationForm(UserCreationForm):
    """Registration form for delivery agents with vehicle and license details"""
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    vehicle_type = forms.ChoiceField(
        choices=DeliveryAgent.VEHICLE_TYPE_CHOICES,
        required=True,
        widget=forms.Select
    )
    vehicle_number = forms.CharField(max_length=20, required=True)
    driving_license = forms.CharField(max_length=50, required=True)
    availability_status = forms.ChoiceField(
        choices=[('True', 'Available'), ('False', 'Not Available')],
        widget=forms.RadioSelect,
        initial='True',
        required=True
    )
    id_proof = forms.FileField(required=False)
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'address', 
                  'vehicle_type', 'vehicle_number', 'driving_license', 
                  'availability_status', 'password1', 'password2', 'id_proof']
    
    def clean_phone(self):
        """Validate phone number is exactly 10 digits"""
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{10}$', phone):
            raise ValidationError('Phone number must be exactly 10 digits.')
        return phone
    
    def clean_email(self):
        """Validate email format and uniqueness"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super(DeliveryAgentRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update user profile type
            user.profile.user_type = 'delivery_agent'
            user.profile.phone = self.cleaned_data['phone']
            user.profile.save()
            
            # Create delivery agent profile
            DeliveryAgent.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                vehicle_type=self.cleaned_data['vehicle_type'],
                vehicle_number=self.cleaned_data['vehicle_number'],
                driving_license=self.cleaned_data['driving_license'],
                availability_status=self.cleaned_data['availability_status'] == 'True',
                id_proof=self.cleaned_data.get('id_proof')
            )
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

