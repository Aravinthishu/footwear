from django.contrib import admin
from .models import Product, Size

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'normal_price', 'discount', 'final_price', 'stock', 'sub_category', 'is_active')
    search_fields = ('name', 'sku', 'description')
    list_filter = ('sub_category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    ordering = ('-created_at',)  # Order by creation date, most recent first
