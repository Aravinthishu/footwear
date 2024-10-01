from django.db import models
from product.models import *
from django.contrib.auth.models import User
from accounts.models import *
from django.utils import timezone

# Create your models here.

#Whishlist
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensures a user can't add the same product twice

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"
    
from django.db import models
from django.contrib.auth.models import User  # Assuming you have a User model for user authentication
from .models import Product  # Import the Product model

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Associate the cart with a user
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the cart is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the cart is updated

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # Link to the cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"

    def get_total_price(self):
        """Calculate total price for this cart item."""
        return self.product.final_price * self.quantity
    
class CouponCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    shipping_name = models.CharField(max_length=50, blank=True, null=True)  # Shipping name
    shipping_email = models.EmailField(blank=True, null=True)  # Shipping email
    country = models.CharField(max_length=50, blank=True, null=True)  # Country
    state = models.CharField(max_length=50, blank=True, null=True)  # State
    city = models.CharField(max_length=50, blank=True, null=True)   # City
    street = models.CharField(max_length=50, blank=True, null=True)   # Shipping address
    pincode = models.CharField(max_length=10, blank=True, null=True)  # Postal code (Pincode)
    shipping_phone = models.CharField(max_length=10, blank=True, null=True)  # Phone number
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)  # Discount on the order
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)  # Subtotal before discount
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)  # Total amount after discount
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # Payment method
    
    
    items = models.ManyToManyField(CartItem)  # Related cart items
    order_date = models.DateTimeField(default=timezone.now)  # Order date and time
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipping', 'Shipping'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    def calculate_total(self):
        """Calculate the total amount of the order."""
        self.total_amount = self.subtotal - (self.discount or 0)
        return self.total_amount

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order}"