from .models import Wishlist
from .models import CartItem, Cart

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0
    return {'wishlist_count': wishlist_count}


def cart_item_count(request):
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        cart_item_count = 0
    return {'cart_item_count': cart_item_count}


