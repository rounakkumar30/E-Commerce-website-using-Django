from django.urls import path
from accounts.views import cart, login_page, register_page, activate_email, add_to_cart, remove_cart,logout_view

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path('logout/', logout_view, name='logout'),
    path("activate/<email_token>/", activate_email, name="activate_email"),
    path("cart/", cart, name="cart"),
    path("add-to-cart/<uid>/", add_to_cart, name="add_to_cart"),
    path("remove-cart/<uid>/", remove_cart, name="remove_cart"),
]
