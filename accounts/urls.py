from django.urls import path
from accounts.views import *
from . import views  # Import views from the same app
from uuid import UUID



urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path('logout/', logout_view, name='logout'),
    path("activate/<email_token>/", activate_email, name="activate_email"),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("delete_account/", delete_account, name="delete_account"),
    path('change-password/', change_password, name='change_password'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path("reset-password/<str:token>/", reset_password, name="reset_password"),
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<uid>/", add_to_cart, name="add_to_cart"),
    path("remove-cart/<uid>/", remove_cart, name="remove_cart"),
]
