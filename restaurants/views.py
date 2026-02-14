from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Restaurant, MenuItem
from .forms import RestaurantForm, MenuItemForm


def restaurant_list(request):
    """Public restaurant listing page"""
    restaurants = Restaurant.objects.filter(is_approved=True)
    
    # Filtering
    search = request.GET.get('search', '')
    cuisine = request.GET.get('cuisine', '')
    veg_only = request.GET.get('veg', '')
    rating_filter = request.GET.get('rating', '')
    
    if search:
        restaurants = restaurants.filter(name__icontains=search) | restaurants.filter(cuisine__icontains=search)
    if cuisine:
        restaurants = restaurants.filter(cuisine__icontains=cuisine)
    if veg_only:
        restaurants = restaurants.filter(is_veg=True)
    if rating_filter:
        restaurants = restaurants.filter(rating__gte=float(rating_filter))
    
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})


@login_required
def owner_dashboard(request):
    """Dashboard for restaurant owners"""
    if not request.user.profile.is_restaurant_owner:
        messages.error(request, 'Access denied. This page is for restaurant owners only.')
        return redirect('index')
    
    # Get restaurant(s) owned by this user
    restaurants = Restaurant.objects.filter(owner=request.user)
    
    return render(request, 'restaurants/owner_dashboard.html', {
        'restaurants': restaurants,
    })


@login_required
def add_restaurant(request):
    """Add a new restaurant"""
    if not request.user.profile.is_restaurant_owner:
        messages.error(request, 'Only restaurant owners can add restaurants.')
        return redirect('index')
    
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, 'Restaurant added successfully!')
            return redirect('restaurants:owner_dashboard')
    else:
        form = RestaurantForm()
    
    return render(request, 'restaurants/add_restaurant.html', {'form': form})


@login_required
def edit_restaurant(request, restaurant_id):
    """Edit restaurant details"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
    
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('restaurants:owner_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)
    
    return render(request, 'restaurants/edit_restaurant.html', {'form': form, 'restaurant': restaurant})


@login_required
def add_menu_item(request, restaurant_id):
    """Add menu item to restaurant"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('restaurants:manage_menu', restaurant_id=restaurant.id)
    else:
        form = MenuItemForm()
    
    return render(request, 'restaurants/add_menu_item.html', {
        'form': form,
        'restaurant': restaurant
    })


@login_required
def manage_menu(request, restaurant_id):
    """View and manage menu items"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
    menu_items = restaurant.menu_items.all()
    
    return render(request, 'restaurants/manage_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })


@login_required
def delete_menu_item(request, item_id):
    """Delete a menu item"""
    menu_item = get_object_or_404(MenuItem, id=item_id, restaurant__owner=request.user)
    restaurant_id = menu_item.restaurant.id
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('restaurants:manage_menu', restaurant_id=restaurant_id)


def restaurant_detail(request, restaurant_id):
    """Restaurant detail page showing full menu"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_approved=True)
    menu_items = restaurant.menu_items.filter(is_available=True)
    
    # Calorie filtering
    calorie_range = request.GET.get('calorie_range', '')
    if calorie_range:
        if calorie_range == 'low':
            menu_items = menu_items.filter(calories__lte=300, calories__isnull=False)
        elif calorie_range == 'medium':
            menu_items = menu_items.filter(calories__gt=300, calories__lte=600)
        elif calorie_range == 'high':
            menu_items = menu_items.filter(calories__gt=600)
    
    # Sorting
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'calories_low':
        menu_items = menu_items.order_by('calories')
    elif sort_by == 'calories_high':
        menu_items = menu_items.order_by('-calories')
    elif sort_by == 'price_low':
        menu_items = menu_items.order_by('price')
    elif sort_by == 'price_high':
        menu_items = menu_items.order_by('-price')
    
    # Group menu items by category if needed (for now showing all)
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }
    return render(request, 'restaurants/restaurant_detail.html', context)

