from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from accounts.views import reset_password

urlpatterns = [
    path('accounts/', include('accounts.urls')),  # Fixed quotes and missing comma
    path('product/', include('products.urls')), 
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path("reset-password/<str:token>/", reset_password, name="reset_password"),
    
]

# Serving media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
