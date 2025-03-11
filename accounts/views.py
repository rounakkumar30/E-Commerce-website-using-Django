from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required

from accounts.models import Cart, CartItems
from products.models import *

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified.")
            return HttpResponseRedirect(request.path_info)

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('/')  # Redirect to home after login

        messages.warning(request, 'Invalid credentials.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number', '')  # Get phone number
        address = request.POST.get('address', '')  # Get address

        # Check if the user already exists
        if User.objects.filter(username=email).exists():
            messages.warning(request, 'Email is already taken.')
            return redirect('register')

        # Create the user
        user_obj = User.objects.create(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            username=email
        )
        user_obj.set_password(password)
        user_obj.save()

        # Create a profile and store address & phone number
        profile, created = Profile.objects.get_or_create(user=user_obj)
        profile.address = address
        profile.phone_number = phone_number
        profile.save()

        messages.success(request, 'Registration successful!')
        return redirect('login')  

    return render(request, 'accounts/register.html')



def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Profile.DoesNotExist:
        return HttpResponse('Invalid Email Token')
    
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("index")  

    return render(request, "accounts/delete_account.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        address = request.POST.get("address", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()  # Get phone number

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.address = address
        profile.phone_number = phone_number  # Save phone number
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "accounts/edit_profile.html")


def add_to_cart(request, uid):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to add items to the cart.")
        return redirect('login')

    variant = request.GET.get('variant')
    product = get_object_or_404(Product, uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    if variant:
        size_variant = get_object_or_404(SizeVariant, size_name=variant)
        cart_item.size_variant = size_variant

    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart(request):
    cart_items = CartItems.objects.filter(cart__user=request.user, cart__is_paid=False)
    context = {'cart_items': cart_items}
    return render(request, 'accounts/cart.html', context)

def cart_view(request):
    cart_items = CartItems.objects.filter(cart__user=request.user, cart__is_paid=False)
    
    cart_total = sum(item.get_product_price() for item in cart_items)  # Calculate total price
    
    discount = 10  
    final_total = cart_total - discount  # Ensure this is correctly calculated

    # Debugging Print Statements
    print("Cart Items:", cart_items)
    print("Cart Total:", cart_total)
    print("Final Total:", final_total)

    return render(request, "accounts/cart.html", {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "discount": discount,
        "final_total": final_total,
    })


def remove_cart(request, uid):  # Change 'cart_item_uid' to 'uid'
    try:
        cart_item = get_object_or_404(CartItems, uid=uid)
        cart_item.delete()
    except Exception as e:
        print(f"Error removing cart item: {e}")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
