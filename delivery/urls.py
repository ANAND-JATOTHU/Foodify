from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('dashboard/', views.delivery_dashboard, name='dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('reject/<int:order_id>/', views.reject_order, name='reject_order'),
    path('pickup/<int:order_id>/', views.mark_as_picked, name='mark_as_picked'),
    path('deliver/<int:order_id>/', views.mark_as_delivered, name='mark_as_delivered'),
    path('route/<int:order_id>/', views.route_map_view, name='route_map'),
    path('location/update/', views.update_agent_location, name='update_location'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
]
