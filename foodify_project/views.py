from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    """Landing page"""
    return render(request, 'index.html')


def test_credentials(request):
    """Test credentials page - shows login details for all test accounts"""
    return render(request, 'test_credentials.html')


def contact(request):
    """Contact page with email sending functionality"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Prepare email content
        email_subject = f'Foodify Contact Form: {subject}'
        email_message = f'''
New contact form submission from Foodify website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
        '''
        
        try:
            # Send email to your address
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['anandhyd2006@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, f'Thanks {name}! We received your message and will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again or email us directly.')
            print(f"Email error: {e}")  # For debugging
        
        return redirect('contact')
    
    return render(request, 'contact.html')
