from django.contrib import admin
from .models import Restaurant, MenuItem, Favorite


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'cuisine', 'rating', 'location', 'is_approved', 'created_at')
    list_filter = ('is_veg', 'is_approved', 'cuisine', 'created_at')
    search_fields = ('name', 'cuisine', 'location', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_approved',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_veg', 'is_available', 'created_at')
    list_filter = ('is_veg', 'is_available', 'created_at')
    search_fields = ('name', 'restaurant__name')
    readonly_fields = ('created_at',)
    list_editable = ('is_available',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'restaurant__name')
