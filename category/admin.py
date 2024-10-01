from django.contrib import admin
from .models import SuperCategory, MainCategory, SubCategory

# SuperCategory admin
@admin.register(SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Display fields in the list view
    search_fields = ('name',)  # Add search functionality
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate the slug field from the name

# MainCategory admin
@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Display fields in the list view
    search_fields = ('name',)  # Add search functionality
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate the slug field from the name

# SubCategory admin
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Display fields in the list view
    search_fields = ('name',)  # Add search functionality
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate the slug field from the name
