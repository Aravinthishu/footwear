from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages  # For flash messages
from orders.models import Order, OrderDetails

# Create your views here.


def profile_view(request, username=None):
    if username:
        # Get the profile of the specified user
        user = get_object_or_404(User, username=username)
        profile = user.profile
    else:
        if request.user.is_authenticated:  # Check if the user is authenticated
            profile = request.user.profile  # Get the user's profile
            
            # Get all orders of the authenticated user
            orders = Order.objects.filter(user=request.user).order_by('-order_date')  # Order by date, if needed
            order_details_list = []  # To store all order details

            # Loop through each order and get its order details
            for order in orders:
                order_details = OrderDetails.objects.filter(order=order)
                order_details_list.extend(order_details)  # Add each order's details to the list

            # Count the number of completed and canceled orders
            completed_orders_count = Order.objects.filter(user=request.user, status='Completed').count()
            canceled_orders_count = Order.objects.filter(user=request.user, status='Cancelled').count()
            print(completed_orders_count)
            
        else:
            return redirect('account_login')  # Redirect to login if not authenticated
    
    # Render the profile page with the necessary context
    context = {
        'profile': profile,
        'orders': orders if request.user.is_authenticated else [],  # Only include orders if authenticated
        'order_details': order_details_list,  # Include order details in the context
        'completed_orders_count': completed_orders_count if request.user.is_authenticated else 0,
        'canceled_orders_count': canceled_orders_count if request.user.is_authenticated else 0,
    }
    return render(request, 'accounts/profile.html', context)



def profile_update(request):
    # Get the user's profile
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Retrieve form data
        pickup_name = request.POST.get('pickup_name')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        city = request.POST.get('city')
        delivery_address = request.POST.get('delivery_address')
        company_name = request.POST.get('company_name')

        # Update the profile fields
        profile.pickup_name = pickup_name
        profile.user.username = name
        profile.user.email = email  # Assuming you want to update this field
        profile.phone = phone
        profile.country = country
        profile.city = city
        profile.delivery_address = delivery_address
        profile.company_name = company_name

        # Handle image upload
        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        # Save the changes
        profile.save()

        # Use messages framework to show a success message
        messages.success(request, 'Profile updated successfully!')

        # Render the same page with updated profile
        return render(request, 'accounts/profile.html', {'profile': profile})

    # If GET request, just render the profile page
    return render(request, 'accounts/profile.html', {'profile': profile})


    

    
    
