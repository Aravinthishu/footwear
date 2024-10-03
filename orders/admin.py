from django.contrib import admin
from .models import *
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Number of empty forms to display

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'size',  'get_total_price')
    search_fields = ('product__name',)
    list_filter = ('cart',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'
    
class CartItemInline(admin.TabularInline):
    model = Order.items.through  # Allows you to add cart items in the Order admin view
    extra = 1  # Number of empty rows to display for adding new CartItems

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 1  # Number of extra blank fields to show for related order details
    readonly_fields = ('price', 'total')  # Fields that are read-only in the admin
    can_delete = False  # Prevent deleting order details from the order in admin

# Custom admin for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'subtotal', 'discount', 'total_amount', 'payment_method', 'is_finished')
    list_filter = ('status', 'order_date', 'is_finished')  # Filter options in the sidebar
    search_fields = ('user__username', 'shipping_email', 'shipping_name')  # Searchable fields
    readonly_fields = ('order_date', 'total_amount')  # Fields that should not be editable in admin
    inlines = [OrderDetailsInline]  # Add inline order details to the order admin
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'order_date', 'status', 'is_finished')
        }),
        ('Shipping Details', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'street', 'city', 'state', 'country', 'pincode')
        }),
        ('Payment and Pricing', {
            'fields': ('subtotal', 'discount', 'total_amount', 'payment_method')
        }),
    )
    actions = ['mark_as_completed', 'mark_as_cancelled']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_as_completed.short_description = 'Mark selected orders as completed'

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
    mark_as_cancelled.short_description = 'Mark selected orders as cancelled'


# Register models with custom admin settings
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails)
admin.site.register(Wishlist)
admin.site.register(CouponCode)
