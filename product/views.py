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

def search(request):
    query = request.GET.get('q')  # Get the search term from the form input
    if query:
        # Search for products containing the query in their name or description
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.none()  # Return an empty QuerySet if no query
    
    # Render the template and pass the list of matching products
    return render(request, 'product/search_results.html', {'products': products, 'query': query})