from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import uuid
from django.core.mail import send_mail
from django.conf import settings




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

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to profile page after change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')  # Redirect to Profile Page
    success_message = "Your password has been changed successfully!"  # Success Message

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully!")
        return super().form_valid(form)
    
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            token = str(uuid.uuid4())  # Generate a unique token
            profile = Profile.objects.get(user=user)
            profile.email_token = token
            profile.save()

            reset_url = f"{request.build_absolute_uri('/reset-password/')}{token}/"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Password reset email has been sent.")
            return redirect("login")

        messages.error(request, "No account found with this email.")
    return render(request, "accounts/forgot_password.html")


def reset_password(request, token):
    print(f"Token received: {token}")
    profile = Profile.objects.filter(email_token=token).first()
    
    if not profile:
        messages.error(request, "Invalid or expired token.")
        return redirect("forgot_password")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(f"/reset-password/{token}/")

        user = profile.user
        user.set_password(new_password)
        user.save()

        profile.email_token = ""  # Reset token after use
        profile.save()

        messages.success(request, "Password has been reset successfully.")
        return redirect("login")

    return render(request, "accounts/reset_password.html", {"token": token})


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

    size_variant = None
    if variant:
        size_variant = get_object_or_404(SizeVariant, size_name=variant)

    # Ensure size_variant is included in get_or_create
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product, size_variant=size_variant)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    cart_items = CartItems.objects.filter(cart__user=request.user, cart__is_paid=False)
    context = {'cart_items': cart_items}
    return render(request, 'accounts/cart.html', context)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.cart_items.all()

    cart_total = 0
    for item in cart_items:
        cart_total += item.get_product_price()

    discount_percentage = 10  # 10% discount
    discount_amount = (discount_percentage / 100) * cart_total
    final_total = cart_total - discount_amount

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'discount': discount_amount,
        'final_total': final_total,
    }
    return render(request, 'accounts/cart.html', context)


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
