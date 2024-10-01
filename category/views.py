from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from product.models import *

# Create your views here.

def new_product_view(request):
    product_list = Product.objects.all()
    return render(request, 'category/new_products.html', {'product_list': product_list})

def main_category_view(request, slug):
    main_category = get_object_or_404(MainCategory, slug=slug)
    product_list = Product.objects.filter(main_category=main_category)

    return render(request, 'category/main_category.html', {'category': main_category, 'product_list': product_list})

def super_category_view(request, slug):
    super_category = get_object_or_404(SuperCategory, slug=slug)
    product_list = Product.objects.filter(super_category=super_category)

    return render(request, 'category/main_category.html', {'category': super_category, 'product_list': product_list})
  