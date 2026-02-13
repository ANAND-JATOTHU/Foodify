from django.contrib import admin
from .models import PaymentTransaction, PaymentNotification


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Admin interface for payment transactions"""
    list_display = [
        'transaction_id',
        'order',
        'customer',
        'restaurant',
        'amount',
        'payment_method',
        'status',
        'created_at',
    ]
    list_filter = [
        'status',
        'payment_method',
        'created_at',
        'restaurant',
    ]
    search_fields = [
        'transaction_id',
        'order__id',
        'customer__username',
        'customer__email',
        'restaurant__name',
    ]
    readonly_fields = [
        'transaction_id',
        'created_at',
        'updated_at',
        'completed_at',
    ]
    fieldsets = (
        ('Transaction Info', {
            'fields': ('transaction_id', 'order', 'customer', 'restaurant')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'amount', 'currency', 'status')
        }),
        ('Gateway Data', {
            'fields': ('gateway_response',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
    """Admin interface for payment notifications"""
    list_display = [
        'title',
        'recipient',
        'notification_type',
        'is_read',
        'created_at',
    ]
    list_filter = [
        'notification_type',
        'is_read',
        'created_at',
    ]
    search_fields = [
        'title',
        'message',
        'recipient__username',
    ]
    readonly_fields = [
        'created_at',
        'read_at',
    ]
    ordering = ['-created_at']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        """Bulk action to mark notifications as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
