from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    """Landing page"""
    return render(request, 'index.html')


def test_credentials(request):
    """Test credentials page - shows login details for all test accounts"""
    return render(request, 'test_credentials.html')


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # In production, you'd send an email here
        messages.success(request, f'Thanks {name}! We received your message and will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')
