from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, SizeVariant
from accounts.models import Cart, CartItems
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}

        size = request.GET.get('size')
        if size:
            price = product.get_product_price_by_size(size)
            context.update({
                'selected_size': size,
                'updated_price': price
            })

        return render(request, 'product/product.html', context)

    except Product.DoesNotExist:
        return render(request, 'product/product.html', {'error': 'Product not found'}, status=404)

    except Exception as e:
        print(f"Error in get_product: {e}")
        return render(request, 'product/product.html', {'error': 'An error occurred'}, status=500)
