from django.urls import path
from products.views import get_product  # Import the correct view
from django.conf import settings
from django.conf.urls.static import static
from products.api_views import search_products
from .views import search_results

urlpatterns = [
    path('product/<slug:slug>/', get_product, name='get_product'),
    path("api/search/", search_products, name="search_products"),
    path('search/', search_results, name='search_results'),
    
]
