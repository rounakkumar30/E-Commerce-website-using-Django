from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from base.models import BaseModel  # Explicit import instead of wildcard
from products.models import Product, ColorVariant, SizeVariant  # Explicit imports

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []

        for cart_item in cart_items:
            price.append(cart_item.product.price)

            if cart_item.color_variant:
                price.append(cart_item.color_variant.price)

            if cart_item.size_variant:
                price.append(cart_item.size_variant.price)

        print(price)  # Debugging line (remove in production)
        return sum(price)


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, blank=True, null=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)  # Added quantity field

    def get_product_price(self):
        price = self.product.price  # Base product price

        if self.color_variant:
            price += self.color_variant.price

        if self.size_variant:
            price += self.size_variant.price

        total_price = price * self.quantity  # Multiply by quantity
        
        print(f"Product: {self.product.name}, Price: {price}, Quantity: {self.quantity}, Total: {total_price}")  # Debugging

        return total_price



@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(f"Error in send_email_token: {e}")
