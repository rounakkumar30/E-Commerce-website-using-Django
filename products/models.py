from django.db import models
from django.utils.text import slugify
from base.models import BaseModel

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.color_name  
    
class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    
    def get_product_price_by_size(self, size):
        return self.price + SizeVariant.objects.get(size_name=size).price

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product/")
