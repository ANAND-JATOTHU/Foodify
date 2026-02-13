from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Customer views
    path('history/', views.payment_history, name='payment_history'),
    path('detail/<int:transaction_id>/', views.payment_detail, name='payment_detail'),
    
    # Restaurant owner views
    path('dashboard/', views.owner_payment_dashboard, name='owner_dashboard'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_read'),
]
