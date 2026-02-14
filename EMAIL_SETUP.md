# Email Configuration Instructions

## Current Setup (Development)
The contact form is currently using Django's **console backend**. This means emails will be printed in the terminal/console where `python manage.py runserver` is running, instead of actually being sent.

This is perfect for testing!

## To Enable Real Email Sending (Production)

### Step 1: Enable Gmail App Password
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Click **App passwords**
5. Select app: **Mail**, Device: **Other** (Django/Foodify)
6. Copy the 16-character password generated

### Step 2: Update .env File
Add this line to your `.env` file:
```
EMAIL_HOST_PASSWORD=your_16_character_app_password_here
```

### Step 3: Update settings.py
In `foodify_project/settings.py`, find the email configuration section and:

**Comment out this line:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Uncomment these lines:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'anandhyd2006@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
```

### Step 4: Restart Server
```bash
python manage.py runserver
```

## Testing
1. Go to: http://127.0.0.1:8000/contact/
2. Fill out the contact form
3. Submit

**Development mode:** Check your terminal for the email output
**Production mode:** Check anandhyd2006@gmail.com inbox for the email

## Contact Information Displayed
- **Phone**: +91 81210 93531
- **Email**: anandhyd2006@gmail.com
- **Address**: Survey No -8/A Medbowli, Meerpet, Telangana 500097
