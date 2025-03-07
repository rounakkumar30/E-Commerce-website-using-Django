from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404
from .models import Product
import json

@csrf_exempt
def search_products(request):
    if request.method == "GET":
        query = request.GET.get("q", "").strip()
        if not query:
            return JsonResponse({"error": "No search query provided"}, status=400)

        products = Product.objects.filter(product_name__icontains=query)
        results = [
            {
                "id": product.id,
                "name": product.product_name,
                "price": product.price,
                "image": product.product_images.first().image.url if product.product_images.exists() else None
            }
            for product in products
        ]

        return JsonResponse({"results": results})
