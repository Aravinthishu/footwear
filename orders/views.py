from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import F


@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Create the wishlist item if it doesn't already exist
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        # If the item is created, display a success message
        if created:
            messages.success(request, f'Product has been added to your wishlist successfully!')
        
        print(messages)

        # Redirect back to the home page or another desired view
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.filter(user=request.user, product=product).delete()
        messages.success(request, f'Product has been removed from your wishlist!')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))


@login_required
def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
        return render(request, 'orders/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return render(request, 'wishlist.html', {'error': 'You need to log in to view your wishlist.'})
    

@login_required
def add_to_cart(request, product_id):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to your cart.")
        return redirect('login')  

    product = get_object_or_404(Product, id=product_id)

    # Retrieve the quantity from the POST data, default to 1 if not provided
    quantity = int(request.POST.get('quantity', 1))
    size_name = request.POST.get('size')
    
    # Check if size is selected
    if not size_name:
        messages.error(request, "Please select a size.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('product', args=[product_id])))

    # Validate quantity (ensure it's a positive integer)
    if quantity <= product.stock:
        messages.error(request, "Quantity must be at least 1.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('product', args=[product_id])))

    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Ensure the size exists in the database
    size = get_object_or_404(Size, size=size_name)

    # Get or create the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)

    # Update the quantity
    cart_item.quantity += quantity  # Always add the specified quantity
    cart_item.save()  # Save the cart item

    messages.success(request, f"{product.name} has been added to your cart.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('product', args=[product_id])))


@login_required
def cart_view(request):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Initialize sizes as an empty list to handle cases when the cart is empty
    sizes = []

    if cart_items.exists():
        for item in cart_items:
            item.sizes = item.product.sizes.all()  # Fetch the related sizes for each product
            sizes = item.sizes  # Set the sizes to the first item's sizes (just for the example)

    # Calculate the subtotal
    subtotal = sum(item.get_total_price() for item in cart_items)
    
    # Initialize coupon variables
    coupon = None
    discount_amount = Decimal('0.00')  # Use Decimal for currency-related values
    final_total = subtotal  # Final total after applying discount

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        print(f"Coupon code entered: {coupon_code}")

        try:
            # Fetch the coupon if it exists and is active
            coupon = CouponCode.objects.get(code=coupon_code, active=True)
            
            # Ensure the coupon is within the valid date range
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                discount_amount = (coupon.discount / Decimal('100.00')) * subtotal
                final_total = subtotal - discount_amount
                print(f"Discount applied: {discount_amount}, Final total: {final_total}")
            else:
                # Coupon is expired
                coupon = None
                print("Coupon is expired.")
        
        except CouponCode.DoesNotExist:
            # Handle case where the coupon code is invalid
            coupon = None
            print("Invalid coupon code.")
    
    # Check if there's an existing unfinished order for the user
    try:
        current_order = Order.objects.filter(user=request.user, is_finished=False).first()
        
        if current_order:
            # If there is an existing unfinished order, update it
            current_order.discount = discount_amount
            current_order.subtotal = subtotal
            current_order.total_amount = final_total
            current_order.order_date = timezone.now()  # Update the order date if necessary
            current_order.items.set(cart_items) 
            current_order.save()
            print(f"Existing order updated: {current_order}")
        else:
            # If no unfinished order, create a new one
            new_order = Order.objects.create(
                user=request.user,
                discount=discount_amount,
                subtotal=subtotal,
                total_amount=final_total,
                order_date=timezone.now(),
                is_finished=False
            )
            new_order.items.set(cart_items)  # Use .set() to assign M2M field
            print(f"New order created: {new_order}")
        
    except Exception as e:
        print(f"Something went wrong: {str(e)}")
    
    # Render the cart template with context data
    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'final_total': final_total,
        'coupon': coupon,
        'sizes': sizes,  # Use the initialized sizes list
    })





def remove_from_cart(request, cart_item_id):
    # Remove an item from the cart
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    # Ensure the cart item belongs to the user's cart
    if cart_item.cart.user == request.user:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    else:
        messages.error(request, "You cannot remove this item from the cart.")

    # Redirect to the cart page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))


@csrf_exempt  # Use csrf_exempt if CSRF token isn't handled (though not recommended for production)
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')

        try:
            cart_item = CartItem.objects.get(id=item_id)
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            cart_item.save()

            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@require_POST
def update_cart_item_size(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        new_size_value = request.POST.get('size')
        
        # Fetch the Size instance based on the submitted value
        new_size = get_object_or_404(Size, size=new_size_value)  # Adjust 'name' based on your Size model's field
        
        # Assign the Size instance to the CartItem
        cart_item.size = new_size
        cart_item.save()  # Save the updated cart item
        
        return redirect('cart')  # Redirect back to the cart view or another appropriate page

from django.shortcuts import get_object_or_404, render
from decimal import Decimal


def checkout_view(request):
    # Get the user's cart and calculate the subtotal
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = sum(item.get_total_price() for item in cart_items)
    
    
    # Check if there's an existing unfinished order
    order = Order.objects.filter(user=request.user, is_finished=False).first()
    
    try:
        if order:
            # If an order exists, apply its discount
            discount_amount = order.discount
            final_total = order.total_amount
        else:
            # No existing order, set default values
            discount_amount = 0
            final_total = subtotal

        if request.method == 'POST':
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            street = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            pincode = request.POST.get('pincode')
            payment_method = request.POST.get('payment-method')


            # If there's an existing unfinished order, update it
            if order:
                order.shipping_name = name
                order.shipping_email = email
                order.shipping_phone = phone
                order.street = street
                order.city = city
                order.state = state
                order.country = country
                order.pincode = pincode
                order.discount = discount_amount
                order.subtotal = subtotal
                order.total_amount = final_total
                order.order_date = timezone.now()
                order.status = 'Processing'
                order.payment_method = payment_method
                order.is_finished = True
                order.items.set(cart_items)
                order.save()
            else:
                # Otherwise, create a new order
                order = Order.objects.create(
                    user=request.user,
                    shipping_name=name,
                    shipping_email=email,
                    shipping_phone=phone,
                    street=street,
                    city=city,
                    state=state,
                    country=country,
                    pincode=pincode,
                    discount=discount_amount,
                    subtotal=subtotal,
                    total_amount=final_total,
                    order_date=timezone.now(),
                    status='Processing',
                    payment_method=payment_method,
                    is_finished=True
                )

            # Add cart items to the order and create OrderDetails for each cart item
            order.items.set(cart_items)
            order.save()

            for cart_item in cart_items:
                OrderDetails.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.final_price,
                    size = cart_item.size,
                    total=cart_item.get_total_price()
                )
                # Update the product's quantity
                product = Product.objects.filter(id=cart_item.product.id).update(
                    stock=F('stock') - cart_item.quantity
                )

            # Empty the cart after the order is placed
            cart.delete()
            # Send a confirmation email to the user
            subject = 'Order Confirmation'
            message = f'Thank you for your order, {name}!\n\n' \
                      f'Your order details:\n' \
                      f'Subtotal: {subtotal}\n' \
                      f'Discount: {discount_amount}\n' \
                      f'Total: {final_total}\n\n' \
                      f'We are processing your order and will notify you when it ships.'

            send_mail(
                subject,
                message,
                settings.ADMIN_EMAIL,  # From email
                [email],  # To email
                fail_silently=False,
            )
            

            # Redirect to the order confirmation page
            return render(request, 'orders/order_confirmation.html', {'order': order})
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Render the checkout template
    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'final_total': final_total,
    })

def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    print('order-id:',order_id)

    if request.method == 'POST':
        order.status = 'Cancelled'  # Update the status to 'Cancelled'
        order.save()
        messages.success(request, f"Your Order(#{order.id}) has been Cancelled.")
        return redirect('profile')  # Redirect to the order list page

    
    return HttpResponse(status=405)  # Method not allowed for non-POST requests

def order_view(request, order_id):
    orders = get_object_or_404(Order, id=order_id, user=request.user)
    order_details_list = OrderDetails.objects.filter(order=orders)

    # Calculate total prices for each order item
    for item in order_details_list:
        item.total_price = item.product.final_price * item.quantity

    return render(request, 'orders/order_view.html', {
        'orders': orders,
        'order_details': order_details_list
    })