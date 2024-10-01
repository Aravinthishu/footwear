from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from orders.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    sizes = product.sizes.all()  

    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    print(wishlist_item)

    context = {
        'product': product,
        'sizes': sizes,
        'wishlist': wishlist_item  
    }

    return render(request, 'product/product-view.html', context)