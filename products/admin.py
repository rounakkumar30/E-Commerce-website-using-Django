from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Category)
# Inline admin for Product Images
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage  # Fixed assignment operator

# Admin for Product with Product Images Inline
class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price']
    inlines = [ProductImageAdmin]

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display=['color_name','price']
    model=ColorVariant
    
    
@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display=['size_name','price']
    model=SizeVariant    


admin.site.register(Product,ProductAdmin)


admin.site.register(ProductImage)

# admin.site.register(Coupon)
