from django.urls import path
from .views import *

urlpatterns = [
    path('product/<str:slug>/',product_view, name='product'),

    
]