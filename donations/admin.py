from django.contrib import admin
from .models import Donation, DonationProof, Notification

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'donor', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('food_name', 'address', 'donor__username')

@admin.register(DonationProof)
class DonationProofAdmin(admin.ModelAdmin):
    list_display = ('donation', 'uploaded_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
