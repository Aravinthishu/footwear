from django.shortcuts import render, get_object_or_404
from .models import *
from product.models import *
from accounts.models import *
from orders.models import Wishlist

# Create your views here.


def home_view(request, username = None):
    hero_section = HeroSection.objects.all()
    product_list = Product.objects.all()
    # Initialize wishlist as an empty list if user is not authenticated
    
    home_banner = HomeBanner.objects.all()
    home_banner2 = HomeBanner2.objects.all()[:4]  # Fetch 4 banners
    user_wishlist = []
    
    if request.user.is_authenticated:
        # Get the product IDs from the wishlist items for the authenticated user
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product__id', flat=True)
    

    if username :
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            profile = None
        
    context = {
        'hero_section': hero_section,
        'product_list': product_list,
        'profile': profile,
        'wishlist': user_wishlist,
        'home_banner': home_banner,
        'home_banner2': home_banner2,
    }
        
    return render(request, 'home/home.html', context)


