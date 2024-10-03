from django.urls import path
from .views import *

urlpatterns = [
    path('add-to-wishlist/<int:product_id>/',add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name='remove-from-wishlist'),
    path('wishlist/', wishlist_view, name="wishlist"),
    
    #add to cart
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name="remove_from_cart"),
    path('cart/', cart_view, name="cart"),
    path('cart/update_quantity/', update_quantity, name='update_quantity'),
    path('update-cart-item-size/<int:item_id>/', update_cart_item_size, name='update_cart_item_size'),
    path('checkout/', checkout_view, name='checkout'),
    
    #order
    path("order-cancel/<int:order_id>", order_cancel, name="order_cancel"),
    path('order-view/<int:order_id>', order_view, name="order_view"),

    
]