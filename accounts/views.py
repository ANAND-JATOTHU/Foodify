from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, DeliveryAgentRegistrationForm


def login_view(request):
    """Login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.profile.is_restaurant_owner:
                return redirect('restaurants:owner_dashboard')
            elif user.profile.is_delivery_agent:
                return redirect('delivery:dashboard')
            else:
                # Customer goes to home page
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login_signup.html')


def register(request):
    """Registration page"""
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        
        # Use delivery agent form for delivery agent registration
        if user_type == 'delivery_agent':
            form = DeliveryAgentRegistrationForm(request.POST, request.FILES)
        else:
            form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Show success message for delivery agents
            if user.profile.is_delivery_agent:
                messages.success(request, 'Delivery Agent Registered Successfully')
                return redirect('delivery:dashboard')
            elif user.profile.is_restaurant_owner:
                return redirect('restaurants:owner_dashboard')
            else:
                return redirect('index')
        else:
            # Pass form errors to template
            return render(request, 'accounts/login_signup.html', {'form': form, 'errors': form.errors})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/login_signup.html', {'form': form})


@login_required
def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

