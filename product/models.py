from django.db import models
from category.models import * 
from tinymce.models import HTMLField
# Create your models here.



class Size(models.Model):
    size = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.size


class Product(models.Model):
    name = models.CharField(max_length=255)
    small_description = HTMLField(blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)  # Original price
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Discount amount
    final_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Final price after discount
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    stock = models.PositiveIntegerField()  # Available stock
    image = models.ImageField(upload_to='products/')  # Main product image
    extra_images = models.ImageField(upload_to='products/extra/', blank=True, null=True)  # Extra image 1
    extra_image_2 = models.ImageField(upload_to='products/extra/', blank=True, null=True)  # Extra image 2
    extra_image_3 = models.ImageField(upload_to='products/extra/', blank=True, null=True)  # Extra image 3
    extra_image_4 = models.ImageField(upload_to='products/extra/', blank=True, null=True)  # Extra image 4
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')  # Related sub-category
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # Related main category
    super_category = models.ForeignKey(SuperCategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # Related super category
    slug = models.SlugField(unique=True)  # Slug for SEO-friendly URLs
    sizes = models.ManyToManyField(Size, related_name='products')  # Many-to-many relationship with sizes
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated
    is_active = models.BooleanField(default=True)  # Product availability

    def save(self, *args, **kwargs):
        # Calculate final price by subtracting the discount percentage
        if self.discount:
            self.final_price = self.normal_price - (self.normal_price * (self.discount / 100))
        else:
            self.final_price = self.normal_price
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name