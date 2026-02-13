from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('place/', views.place_order, name='place_order'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/track/', views.track_order, name='track_order'),
    path('<int:order_id>/agent-location/', views.get_agent_location, name='get_agent_location'),
    # Restaurant owner order management
    path('manage/', views.owner_orders, name='owner_orders'),
    path('manage/<int:order_id>/', views.owner_order_detail, name='owner_order_detail'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    # Stripe payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    # Stripe API endpoints
    path('api/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('api/confirm-payment/', views.confirm_payment, name='confirm_payment'),
]
