from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_list, name='list'),
    path('<int:restaurant_id>/', views.restaurant_detail, name='detail'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('add/', views.add_restaurant, name='add_restaurant'),
    path('edit/<int:restaurant_id>/', views.edit_restaurant, name='edit_restaurant'),
    path('<int:restaurant_id>/menu/', views.manage_menu, name='manage_menu'),
    path('<int:restaurant_id>/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
]
