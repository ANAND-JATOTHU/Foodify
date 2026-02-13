from django.contrib import admin
from .models import UserProfile, DeliveryAgent


# Register UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


# Register DeliveryAgent model
@admin.register(DeliveryAgent)
class DeliveryAgentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'phone', 'vehicle_type', 'availability_status', 'created_at')
    list_filter = ('vehicle_type', 'availability_status', 'created_at')
    search_fields = ('full_name', 'user__username', 'phone', 'vehicle_number', 'driving_license')
    readonly_fields = ('created_at', 'updated_at', 'total_deliveries', 'total_earnings')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'phone')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Vehicle Details', {
            'fields': ('vehicle_type', 'vehicle_number', 'driving_license')
        }),
        ('Status', {
            'fields': ('availability_status',)
        }),
        ('Documents', {
            'fields': ('id_proof',)
        }),
        ('Statistics', {
            'fields': ('total_deliveries', 'total_earnings', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

