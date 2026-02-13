from django.contrib import admin
from .models import Cart, Order, OrderItem, Payment


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu_item', 'quantity', 'subtotal', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'menu_item__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'payment_status', 'is_paid', 'grand_total', 'created_at')
    list_filter = ('status', 'payment_status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'restaurant__name')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at', 'payment_intent_id')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'price', 'quantity', 'subtotal')
    search_fields = ('name', 'order__user__username')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'variant', 'total', 'status', 'created')
    list_filter = ('status', 'variant', 'created')
    search_fields = ('order__id', 'billing_email', 'transaction_id')
    readonly_fields = ('transaction_id', 'token', 'created', 'modified')


