from django.contrib import admin
from django.urls import path, include
from . views import *

urlpatterns = [
   path('main-category/<str:slug>/', main_category_view, name='main_category'),
   path('super-category/<str:slug>/', super_category_view, name='super_category'),
   path('latest-product/', new_product_view, name='latest_product'),
   
]
